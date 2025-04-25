# OptiWeather

## Overview

This project provides a comprehensive simulation and analysis tool for Free Space Optical (FSO) communication systems under various weather conditions. The tool features:

- Real-time animated visualization of signal propagation
- Detailed performance analysis (BER, SNR, attenuation)
- Interactive GUI with parameter controls
- Weather condition modeling (clear, fog, rain, snow)
- Modulation scheme comparison (OOK, PPM, BPSK)

## Features

- **Interactive Simulation Controls**:
  - Adjustable transmission distance (100-5000m)
  - Variable transmitter power (-10 to 20 dBm)
  - Configurable aperture diameter (0.01-0.5m)
  - Selectable data rates (10 Mbps to 10 Gbps)

- **Weather Condition Modeling**:
  - Clear sky
  - Haze
  - Light fog
  - Heavy fog
  - Rain
  - Snow

- **Performance Metrics**:
  - Bit Error Rate (BER) calculations
  - Signal-to-Noise Ratio (SNR)
  - Atmospheric attenuation
  - Received power analysis

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install via pip):

```bash
pip install numpy matplotlib scipy pandas tk
```

### Running the Application

1. Clone the repository:
```bash
git clone https://github.com/mounishkr/OptiWeather.git
```

2. Run the simulator:
```bash
python OptiWeather.py
```

## Usage

1. **Adjust Simulation Parameters**:
   - Use the sliders to set distance, transmitter power, aperture diameter, and data rate
   - Select weather conditions from the radio buttons
   - Choose modulation scheme (OOK, PPM, or BPSK)

2. **Visualization**:
   - The top panel shows real-time signal propagation animation
   - Signal intensity is displayed along the transmission path

3. **Performance Analysis**:
   - The bottom panel shows performance metrics vs distance
   - Metrics include attenuation, SNR, and BER
   - Click "Run Simulation" for detailed analysis

4. **Results Display**:
   - The right panel shows numerical results including:
     - Calculated attenuation
     - Received power
     - Noise power
     - SNR
     - BER

## Technical Details

### Atmospheric Attenuation Models

The simulator implements empirical models for different weather conditions:

- Clear sky: 0.1 dB/km
- Haze: 1.0 dB/km
- Light fog: 5.0 dB/km
- Heavy fog: 20.0 dB/km
- Rain: 10.0 dB/km
- Snow: 15.0 dB/km

### BER Calculations

Bit Error Rate is calculated based on modulation scheme:

- **OOK (On-Off Keying)**:
  ```math
  BER = \frac{1}{2} \text{erfc}\left(\frac{\sqrt{SNR}}{2}\right)
  ```

- **PPM (Pulse Position Modulation)**:
  ```math
  BER = \frac{1}{2} \text{erfc}\left(\frac{\sqrt{SNR}}{4}\right)
  ```

- **BPSK (Binary Phase Shift Keying)**:
  ```math
  BER = \frac{1}{2} \text{erfc}\left(\sqrt{SNR}\right)
  ```

## Screenshots

### Results 



## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by research in Free Space Optical communications
- Built with Python scientific computing stack (NumPy, SciPy, Matplotlib)

## Contact

For questions or suggestions, please contact:
[M.Mounish Kumar] - [mounishkr.com]

Project Link: [https://github.com/mounishkr/OptiWeather](https://github.com/mounishkr/OptiWeather)
