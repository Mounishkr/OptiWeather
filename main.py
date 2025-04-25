import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons
import tkinter as tk
from tkinter import ttk
from scipy.special import erfc
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as colors
from matplotlib import cm
import time
import threading

class FSOSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("FSO Communication Simulator")
        self.root.geometry("1200x800")
        
        # Simulation parameters
        self.distance = 1000  # meters
        self.wavelength = 1550e-9  # 1550 nm
        self.tx_power = 10  # dBm
        self.aperture_diameter = 0.1  # meters
        self.data_rate = 1e9  # 1 Gbps
        self.weather_condition = "clear"
        self.modulation = "OOK"
        
        # Create GUI
        self.create_gui()
        
        # Initialize plots
        self.setup_plots()
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self.start_animation)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def create_gui(self):
        # Create main frames
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        visualization_frame = ttk.LabelFrame(self.root, text="Signal Visualization", padding=10)
        visualization_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        analysis_frame = ttk.LabelFrame(self.root, text="Performance Analysis", padding=10)
        analysis_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control widgets
        self.distance_slider = self.create_slider(control_frame, "Distance (m)", 100, 5000, self.distance)
        self.power_slider = self.create_slider(control_frame, "Tx Power (dBm)", -10, 20, self.tx_power)
        self.aperture_slider = self.create_slider(control_frame, "Aperture Diameter (m)", 0.01, 0.5, self.aperture_diameter)
        self.rate_slider = self.create_slider(control_frame, "Data Rate (Mbps)", 10, 10000, self.data_rate/1e6)
        
        # Weather selection
        ttk.Label(control_frame, text="Weather Condition:").pack(anchor=tk.W)
        self.weather_var = tk.StringVar(value=self.weather_condition)
        weather_options = ["clear", "haze", "light_fog", "heavy_fog", "rain", "snow"]
        for opt in weather_options:
            ttk.Radiobutton(control_frame, text=opt, variable=self.weather_var, 
                           value=opt, command=self.update_weather).pack(anchor=tk.W)
        
        # Modulation selection
        ttk.Label(control_frame, text="Modulation:").pack(anchor=tk.W)
        self.modulation_var = tk.StringVar(value=self.modulation)
        mod_options = ["OOK", "PPM", "BPSK"]
        for opt in mod_options:
            ttk.Radiobutton(control_frame, text=opt, variable=self.modulation_var, 
                           value=opt, command=self.update_modulation).pack(anchor=tk.W)
        
        # Run button
        ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation).pack(pady=10)
        
        # Visualization canvas
        self.fig_vis = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax_vis = self.fig_vis.add_subplot(111)
        self.canvas_vis = FigureCanvasTkAgg(self.fig_vis, master=visualization_frame)
        self.canvas_vis.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Analysis canvas
        self.fig_analysis = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax_analysis = self.fig_analysis.add_subplot(111)
        self.canvas_analysis = FigureCanvasTkAgg(self.fig_analysis, master=analysis_frame)
        self.canvas_analysis.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results display
        self.results_text = tk.Text(control_frame, height=10, width=30)
        self.results_text.pack(fill=tk.X, pady=5)
    
    def create_slider(self, parent, label, min_val, max_val, init_val):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label).pack(anchor=tk.W)
        
        current_value = tk.DoubleVar(value=init_val)
        slider = ttk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                          variable=current_value, command=lambda v: self.update_parameter(label, float(v)))
        slider.pack(fill=tk.X)
        
        value_label = ttk.Label(frame, text=f"{init_val:.2f}")
        value_label.pack(anchor=tk.E)
        
        return (slider, current_value, value_label)
    
    def update_parameter(self, param, value):
        if "Distance" in param:
            self.distance = value
        elif "Power" in param:
            self.tx_power = value
        elif "Aperture" in param:
            self.aperture_diameter = value
        elif "Rate" in param:
            self.data_rate = value * 1e6
        
        # Update label
        for slider in [self.distance_slider, self.power_slider, self.aperture_slider, self.rate_slider]:
            if param in slider[2]['text']:
                slider[2].config(text=f"{value:.2f}")
                break
    
    def update_weather(self):
        self.weather_condition = self.weather_var.get()
    
    def update_modulation(self):
        self.modulation = self.modulation_var.get()
    
    def setup_plots(self):
        # Clear axes
        self.ax_vis.clear()
        self.ax_analysis.clear()
        
        # Setup visualization plot
        self.ax_vis.set_title("FSO Signal Propagation")
        self.ax_vis.set_xlabel("Distance (m)")
        self.ax_vis.set_ylabel("Signal Intensity")
        self.ax_vis.grid(True)
        
        # Setup analysis plot
        self.ax_analysis.set_title("Performance Analysis")
        self.ax_analysis.set_xlabel("Time")
        self.ax_analysis.set_ylabel("Metric Value")
        self.ax_analysis.grid(True)
        
        # Draw initial plots
        self.canvas_vis.draw()
        self.canvas_analysis.draw()
    
    def start_animation(self):
        # Create animation data
        self.x_data = np.linspace(0, self.distance, 100)
        self.y_data = np.zeros_like(self.x_data)
        self.time_data = np.linspace(0, 1, 100)
        
        # Create line objects
        self.line_vis, = self.ax_vis.plot(self.x_data, self.y_data, 'b-', lw=2)
        self.line_analysis, = self.ax_analysis.plot(self.time_data, np.zeros_like(self.time_data), 'r-', lw=2)
        
        # Animation function
        def animate(i):
            # Update signal propagation
            attenuation = self.calculate_attenuation()
            received_power = self.tx_power - attenuation
            noise = self.calculate_noise()
            
            # Simulate signal with noise
            signal = received_power * np.exp(-(self.x_data - self.distance/2)**2 / (2*(self.distance/5)**2))
            noise_component = np.random.normal(0, noise, len(self.x_data))
            self.y_data = signal + noise_component
            
            # Update visualization
            self.line_vis.set_ydata(self.y_data)
            self.ax_vis.set_ylim(0, max(1, np.max(self.y_data)*1.1))
            
            # Update performance metrics
            snr = received_power - noise if noise > 0 else 100
            ber = self.calculate_ber(snr)
            
            # Shift old data and add new point
            y_analysis = self.line_analysis.get_ydata()
            y_analysis = np.roll(y_analysis, -1)
            y_analysis[-1] = ber * 1e6  # Show BER in 1e-6 scale
            self.line_analysis.set_ydata(y_analysis)
            self.ax_analysis.set_ylim(0, max(1, np.max(y_analysis)*1.1))
            
            return self.line_vis, self.line_analysis
        
        # Create animation
        self.ani = FuncAnimation(self.fig_vis, animate, frames=100, interval=100, blit=True)
        self.canvas_vis.draw()
    
    def calculate_attenuation(self):
        """Calculate atmospheric attenuation based on weather conditions"""
        if self.weather_condition == "clear":
            return 0.1 * self.distance / 1000  # dB/km
        elif self.weather_condition == "haze":
            return 1.0 * self.distance / 1000
        elif self.weather_condition == "light_fog":
            return 5.0 * self.distance / 1000
        elif self.weather_condition == "heavy_fog":
            return 20.0 * self.distance / 1000
        elif self.weather_condition == "rain":
            return 10.0 * self.distance / 1000
        elif self.weather_condition == "snow":
            return 15.0 * self.distance / 1000
        else:
            return 0.1 * self.distance / 1000
    
    def calculate_noise(self):
        """Calculate noise power based on system parameters"""
        # Simplified noise model
        weather_factor = {
            "clear": 1.0,
            "haze": 1.2,
            "light_fog": 1.5,
            "heavy_fog": 2.0,
            "rain": 1.8,
            "snow": 2.2
        }.get(self.weather_condition, 1.0)
        
        return 5.0 * weather_factor * np.sqrt(self.data_rate / 1e9)
    
    def calculate_ber(self, snr):
        """Calculate bit error rate based on modulation and SNR"""
        if self.modulation == "OOK":
            return 0.5 * erfc(np.sqrt(10**(snr/10) / 2))
        elif self.modulation == "PPM":
            return 0.5 * erfc(np.sqrt(10**(snr/10) / 4))
        elif self.modulation == "BPSK":
            return 0.5 * erfc(np.sqrt(10**(snr/10)))
        else:
            return 0.5 * erfc(np.sqrt(10**(snr/10) / 2))
    
    def run_simulation(self):
        """Run detailed simulation and update results"""
        # Calculate metrics
        attenuation = self.calculate_attenuation()
        received_power = self.tx_power - attenuation
        noise = self.calculate_noise()
        snr = received_power - noise if noise > 0 else 100
        ber = self.calculate_ber(snr)
        
        # Update results display
        results = f"""=== Simulation Results ===
Distance: {self.distance:.2f} m
Tx Power: {self.tx_power:.2f} dBm
Aperture Diameter: {self.aperture_diameter:.2f} m
Data Rate: {self.data_rate/1e6:.2f} Mbps
Weather: {self.weather_condition}
Modulation: {self.modulation}

Attenuation: {attenuation:.2f} dB
Received Power: {received_power:.2f} dBm
Noise Power: {noise:.2f} dB
SNR: {snr:.2f} dB
BER: {ber:.2e}"""
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)
        
        # Update analysis plot with comprehensive data
        self.ax_analysis.clear()
        
        # Generate range of distances for analysis
        distances = np.linspace(100, 5000, 50)
        attens = [self.calculate_attenuation_for_distance(d) for d in distances]
        snrs = [self.tx_power - a - self.calculate_noise() for a in attens]
        bers = [self.calculate_ber(s) for s in snrs]
        
        # Plot multiple metrics
        self.ax_analysis.plot(distances, attens, 'b-', label='Attenuation (dB)')
        self.ax_analysis.plot(distances, snrs, 'r-', label='SNR (dB)')
        self.ax_analysis.plot(distances, [b*1e6 for b in bers], 'g-', label='BER (1e-6)')
        
        self.ax_analysis.set_title("Performance vs Distance")
        self.ax_analysis.set_xlabel("Distance (m)")
        self.ax_analysis.set_ylabel("Metric Value")
        self.ax_analysis.legend()
        self.ax_analysis.grid(True)
        
        self.canvas_analysis.draw()
    
    def calculate_attenuation_for_distance(self, distance):
        """Helper method to calculate attenuation for arbitrary distance"""
        if self.weather_condition == "clear":
            return 0.1 * distance / 1000
        elif self.weather_condition == "haze":
            return 1.0 * distance / 1000
        elif self.weather_condition == "light_fog":
            return 5.0 * distance / 1000
        elif self.weather_condition == "heavy_fog":
            return 20.0 * distance / 1000
        elif self.weather_condition == "rain":
            return 10.0 * distance / 1000
        elif self.weather_condition == "snow":
            return 15.0 * distance / 1000
        else:
            return 0.1 * distance / 1000

if __name__ == "__main__":
    root = tk.Tk()
    app = FSOSimulator(root)
    root.mainloop()