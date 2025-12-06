"""
Main script to run geopolitical forecasting simulation
Uses WorldModel, CountryAgent, and generates PDF reports
"""
import logging
import os
from datetime import datetime
from src.models.world_model import WorldModel
from src.report_generator import ForecastReportGenerator
from src.configuration import Configuration

# Load configuration
config = Configuration()

# Setup logging from configuration
log_dir = config.log_dir
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"forecast_{timestamp}.log")

logging.basicConfig(
    level=getattr(logging, config.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the complete simulation pipeline"""
    
    # Create reports directory from configuration
    reports_dir = config.report_dir
    os.makedirs(reports_dir, exist_ok=True)
    
    # Initialize World Model
    logger.info("Initializing World Model...")
    model = WorldModel()
    
    # Run complete simulation (exploration + forecasting)
    model.run_simulation()
    
    # Generate PDF Report
    logger.info("Generating PDF report...")
    try:
        # Collect all forecasts from agents
        forecasts_data = model.get_forecasts()
        
        if forecasts_data:
            # Generate PDF report
            report_gen = ForecastReportGenerator()
            report_gen.generate_report(
                scenario=model.scenario,
                forecasts=forecasts_data,
                timestamp=datetime.now()
            )
            logger.info(f"✅ PDF report generated: {report_gen.output_path}")
        else:
            logger.warning("No forecasts available to generate report")
            
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}", exc_info=True)


if __name__ == "__main__":
    main()