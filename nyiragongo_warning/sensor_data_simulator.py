# sensor_data_simulator.py
# Real-time sensor data simulation script for Mount Nyiragongo

import requests
import random
import time
import json
import math
from datetime import datetime, timedelta
import threading
import argparse
import sys

class VolcanicDataSimulator:
    def __init__(self, api_endpoint='http://localhost:8000/api/sensor-data/'):
        self.api_endpoint = api_endpoint
        self.running = False
        
        # Base values for normal conditions
        self.base_seismic = 1.5
        self.base_gas = 200
        self.base_deformation = 5
        self.base_temperature = 800
        
        # Simulation parameters
        self.eruption_cycle = 0
        self.time_factor = 0
        
    def generate_realistic_data(self):
        """Generate realistic volcanic monitoring data with patterns"""
        
        # Add time-based variations
        self.time_factor += 0.1
        
        # Create daily and long-term patterns
        daily_variation = math.sin(self.time_factor * 0.1) * 0.3
        long_term_trend = math.sin(self.time_factor * 0.01) * 0.5
        
        # Generate random variations
        seismic_noise = random.uniform(-0.5, 0.5)
        gas_noise = random.uniform(-50, 50)
        deformation_noise = random.uniform(-2, 2)
        temperature_noise = random.uniform(-100, 100)
        
        # Simulate eruption cycles (every ~500 data points)
        if self.time_factor % 50 < 10:  # Eruption building phase
            eruption_factor = (self.time_factor % 50) / 10
            seismic_multiplier = 1 + eruption_factor * 3
            gas_multiplier = 1 + eruption_factor * 4
            deformation_multiplier = 1 + eruption_factor * 8
            temperature_multiplier = 1 + eruption_factor * 0.5
        else:  # Normal conditions
            seismic_multiplier = 1
            gas_multiplier = 1
            deformation_multiplier = 1
            temperature_multiplier = 1
        
        # Calculate final values
        seismic_activity = max(0, (self.base_seismic + daily_variation + long_term_trend + seismic_noise) * seismic_multiplier)
        gas_emissions = max(0, (self.base_gas + gas_noise) * gas_multiplier)
        ground_deformation = max(0, (self.base_deformation + deformation_noise) * deformation_multiplier)
        temperature = max(0, (self.base_temperature + temperature_noise) * temperature_multiplier)
        
        # Add occasional spikes for realism
        if random.random() < 0.05:  # 5% chance of spike
            seismic_activity *= random.uniform(1.5, 3.0)
            gas_emissions *= random.uniform(1.2, 2.0)
        
        # Add correlation between parameters
        if seismic_activity > 3.0:
            gas_emissions *= 1.5
            temperature *= 1.2
        
        return {
            'seismic_activity': round(seismic_activity, 2),
            'gas_emissions': round(gas_emissions, 1),
            'ground_deformation': round(ground_deformation, 1),
            'temperature': round(temperature, 1),
            'timestamp': datetime.now().isoformat()
        }
    
    def send_data(self, data):
        """Send data to Django API endpoint"""
        try:
            response = requests.post(
                self.api_endpoint,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Data sent successfully - Alert Level: {result.get('alert_level', 'unknown')}")
                return True
            else:
                print(f"✗ Failed to send data: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def simulate_emergency_scenario(self):
        """Simulate a volcanic emergency scenario"""
        print("\n🚨 SIMULATING EMERGENCY SCENARIO 🚨")
        print("Rapidly increasing volcanic activity...")
        
        for i in range(20):
            # Gradually increase activity
            factor = i / 20
            
            emergency_data = {
                'seismic_activity': self.base_seismic + factor * 8,
                'gas_emissions': self.base_gas + factor * 1500,
                'ground_deformation': self.base_deformation + factor * 100,
                'temperature': self.base_temperature + factor * 600,
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_data(emergency_data)
            time.sleep(2)  # Send data every 2 seconds during emergency
            
        print("Emergency scenario simulation completed!")
    
    def simulate_gradual_increase(self, duration_minutes=30):
        """Simulate gradual increase in volcanic activity over time"""
        print(f"\n📈 SIMULATING GRADUAL INCREASE ({duration_minutes} minutes)")
        print("Volcanic activity slowly building up...")
        
        steps = duration_minutes * 2  # Every 30 seconds
        
        for i in range(steps):
            factor = i / steps
            
            data = {
                'seismic_activity': self.base_seismic * (1 + factor * 2),
                'gas_emissions': self.base_gas * (1 + factor * 3),
                'ground_deformation': self.base_deformation * (1 + factor * 5),
                'temperature': self.base_temperature * (1 + factor * 0.3),
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_data(data)
            time.sleep(30)
            
        print("Gradual increase simulation completed!")
    
    def start_simulation(self, interval=30):
        """Start continuous data simulation"""
        self.running = True
        print(f"🌋 Starting Mount Nyiragongo sensor simulation...")
        print(f"📡 Sending data every {interval} seconds to {self.api_endpoint}")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                # Generate and send data
                data = self.generate_realistic_data()
                success = self.send_data(data)
                
                if success:
                    # Display current readings
                    print(f"📊 Seismic: {data['seismic_activity']:.1f} | "
                          f"Gas: {data['gas_emissions']:.0f}ppm | "
                          f"Ground: {data['ground_deformation']:.1f}mm | "
                          f"Temp: {data['temperature']:.0f}°C")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Simulation stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"⚠️ Error in simulation: {e}")
                time.sleep(5)  # Wait before retrying
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False

def main():
    """Main function with command line interface"""
    print("🌋 Mount Nyiragongo Volcanic Data Simulator")
    print("=" * 50)
    
    # Initialize simulator
    simulator = VolcanicDataSimulator()
    
    # Menu options
    while True:
        print("\nSelect simulation mode:")
        print("1. Normal continuous monitoring (30s intervals)")
        print("2. Fast monitoring (5s intervals)")
        print("3. Emergency scenario simulation")
        print("4. Gradual increase simulation")
        print("5. Custom interval monitoring")
        print("6. Test single data point")
        print("7. Generate batch data")
        print("8. Check API connection")
        print("9. Exit")
        
        try:
            choice = input("\nEnter choice (1-9): ").strip()
            
            if choice == '1':
                simulator.start_simulation(30)
            
            elif choice == '2':
                simulator.start_simulation(5)
            
            elif choice == '3':
                simulator.simulate_emergency_scenario()
            
            elif choice == '4':
                try:
                    duration = int(input("Enter duration in minutes (default 30): ") or "30")
                    simulator.simulate_gradual_increase(duration)
                except ValueError:
                    print("Invalid input. Using default 30 minutes.")
                    simulator.simulate_gradual_increase(30)
            
            elif choice == '5':
                try:
                    interval = int(input("Enter interval in seconds: "))
                    if interval > 0:
                        simulator.start_simulation(interval)
                    else:
                        print("Invalid interval. Must be positive.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif choice == '6':
                data = simulator.generate_realistic_data()
                print(f"\nGenerated data: {json.dumps(data, indent=2)}")
                success = simulator.send_data(data)
                print(f"Send result: {'Success' if success else 'Failed'}")
            
            elif choice == '7':
                try:
                    count = int(input("Enter number of data points to generate (default 100): ") or "100")
                    generate_batch_data(count, simulator)
                except ValueError:
                    print("Invalid input. Using default 100 points.")
                    generate_batch_data(100, simulator)
            
            elif choice == '8':
                test_api_connection(simulator)
            
            elif choice == '9':
                print("Goodbye! 👋")
                break
            
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted. Goodbye! 👋")
            break

def generate_batch_data(count=100, simulator=None):
    """Generate batch data for testing"""
    if simulator is None:
        simulator = VolcanicDataSimulator()
    
    batch_data = []
    successful_sends = 0
    
    print(f"Generating and sending {count} data points...")
    print("Progress: ", end="", flush=True)
    
    for i in range(count):
        data = simulator.generate_realistic_data()
        batch_data.append(data)
        
        # Send data and show progress
        if simulator.send_data(data):
            successful_sends += 1
        
        # Show progress every 10 points
        if (i + 1) % 10 == 0:
            print(f"{i + 1}", end="", flush=True)
            if (i + 1) % 50 == 0:
                print(" ", end="", flush=True)
            else:
                print(".", end="", flush=True)
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.5)
    
    print(f"\n\n✅ Batch generation completed!")
    print(f"📊 Total points generated: {count}")
    print(f"📡 Successfully sent: {successful_sends}")
    print(f"❌ Failed sends: {count - successful_sends}")
    
    # Save to file option
    save_choice = input("\nSave generated data to file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = f"volcanic_data_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(batch_data, f, indent=2)
            print(f"💾 Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")

def test_api_connection(simulator):
    """Test API connection and endpoint availability"""
    print("\n🔍 Testing API connection...")
    print(f"📡 Endpoint: {simulator.api_endpoint}")
    
    try:
        # Try a simple GET request first
        response = requests.get(simulator.api_endpoint.replace('/api/sensor-data/', '/api/health/'), timeout=5)
        if response.status_code == 200:
            print("✅ API server is reachable")
        else:
            print(f"⚠️ API server responded with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach API server: {e}")
        return False
    
    # Test with sample data
    print("🧪 Testing with sample data...")
    test_data = {
        'seismic_activity': 2.5,
        'gas_emissions': 350.0,
        'ground_deformation': 8.2,
        'temperature': 950.0,
        'timestamp': datetime.now().isoformat()
    }
    
    success = simulator.send_data(test_data)
    if success:
        print("✅ API endpoint is working correctly")
    else:
        print("❌ API endpoint test failed")
    
    return success

def run_cli():
    """Command line interface for advanced users"""
    parser = argparse.ArgumentParser(description='Mount Nyiragongo Volcanic Data Simulator')
    parser.add_argument('--endpoint', '-e', default='http://localhost:8000/api/sensor-data/',
                        help='API endpoint URL')
    parser.add_argument('--interval', '-i', type=int, default=30,
                        help='Data sending interval in seconds')
    parser.add_argument('--mode', '-m', choices=['normal', 'fast', 'emergency', 'batch'],
                        default='normal', help='Simulation mode')
    parser.add_argument('--count', '-c', type=int, default=100,
                        help='Number of data points for batch mode')
    parser.add_argument('--duration', '-d', type=int, default=30,
                        help='Duration in minutes for gradual increase mode')
    
    args = parser.parse_args()
    
    simulator = VolcanicDataSimulator(args.endpoint)
    
    print(f"🌋 Starting simulation in {args.mode} mode")
    
    try:
        if args.mode == 'normal':
            simulator.start_simulation(args.interval)
        elif args.mode == 'fast':
            simulator.start_simulation(5)
        elif args.mode == 'emergency':
            simulator.simulate_emergency_scenario()
        elif args.mode == 'batch':
            generate_batch_data(args.count, simulator)
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped")

if __name__ == "__main__":
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        run_cli()
    else:
        main()