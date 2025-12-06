"""
PDF Report Generator for Geopolitical Forecasts
Generates professional PDF reports with forecasts and Chain of Thought analysis
"""
import logging
from datetime import datetime
from typing import List, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Indenter
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from src.configuration import Configuration

logger = logging.getLogger(__name__)

# Load configuration
config = Configuration()


class ForecastReportGenerator:
    """Generates PDF reports for geopolitical forecasts"""
    
    def __init__(self, output_path: str = None):
        """
        Initialize report generator
        
        Args:
            output_path: Path to output PDF file. If None, generates timestamp-based name.
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{config.report_dir}/forecast_report_{timestamp}.pdf"
        
        self.output_path = output_path
        
        # Get page size from config
        page_size = A4 if config.report_page_size.upper() == "A4" else letter
        
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#3949ab'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='Subsection',
            parent=self.styles['Heading4'],
            fontSize=12,
            textColor=colors.HexColor('#5e35b1'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Body text with justify
        self.styles.add(ParagraphStyle(
            name='BodyJustify',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))
        
        # Indented text
        self.styles.add(ParagraphStyle(
            name='IndentedText',
            parent=self.styles['BodyText'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))
        
        # Bullet point style (custom name to avoid conflict)
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['BodyText'],
            fontSize=10,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=3
        ))
        
    def add_title_page(self, title: str, subtitle: str = None, scenario: str = None):
        """Add title page to report"""
        # Main title
        self.story.append(Spacer(1, 2*inch))
        self.story.append(Paragraph(title, self.styles['CustomTitle']))
        
        if subtitle:
            self.story.append(Spacer(1, 0.5*inch))
            self.story.append(Paragraph(subtitle, self.styles['CustomSubtitle']))
        
        # Date and scenario
        self.story.append(Spacer(1, 1*inch))
        date_str = datetime.now().strftime("%d %B %Y, %H:%M")
        self.story.append(Paragraph(f"<b>Data wygenerowania:</b> {date_str}", self.styles['BodyJustify']))
        
        if scenario:
            self.story.append(Spacer(1, 0.3*inch))
            self.story.append(Paragraph("<b>Scenariusz Globalny:</b>", self.styles['SectionHeader']))
            # Split long scenario into paragraphs
            for line in scenario.split('\n'):
                if line.strip():
                    self.story.append(Paragraph(line.strip(), self.styles['BodyJustify']))
                    self.story.append(Spacer(1, 6))
        
        self.story.append(PageBreak())
    
    def add_country_forecast(self, country_name: str, forecasts, scenario_weight: int):
        """
        Add complete forecast analysis for a country
        
        Args:
            country_name: Name of the country
            forecasts: ForecastOutput object with 12 and 36 month forecasts
            scenario_weight: Total weight of the scenario
        """
        # Country header
        self.story.append(Paragraph(
            f"Analiza Prognostyczna: {country_name}",
            self.styles['CustomTitle']
        ))
        self.story.append(Spacer(1, 12))
        
        self.story.append(Paragraph(
            f"<b>Waga scenariusza:</b> {scenario_weight}/100",
            self.styles['BodyJustify']
        ))
        self.story.append(Spacer(1, 20))
        
        # Add 12-month forecast
        self._add_forecast_section(forecasts.forecast_12_months, "12 miesięcy")
        
        # Add page break before 36-month forecast
        self.story.append(PageBreak())
        
        # Add 36-month forecast
        self._add_forecast_section(forecasts.forecast_36_months, "36 miesięcy")
        
        # Add page break after each country
        self.story.append(PageBreak())
    
    def _add_forecast_section(self, forecast, timeframe: str):
        """Add a single forecast section (12 or 36 months)"""
        # Timeframe header
        self.story.append(Paragraph(
            f"📅 Prognoza na {timeframe}",
            self.styles['CustomSubtitle']
        ))
        self.story.append(Spacer(1, 12))
        
        # Chain of Thought section
        self.story.append(Paragraph(
            "🔍 CHAIN OF THOUGHT (Wyjaśnialność)",
            self.styles['SectionHeader']
        ))
        
        # Historical facts
        self.story.append(Paragraph("📚 Fakty historyczne i obecne trendy:", self.styles['Subsection']))
        for i, fact in enumerate(forecast.historical_facts, 1):
            self.story.append(Paragraph(f"{i}. {fact}", self.styles['IndentedText']))
        self.story.append(Spacer(1, 12))
        
        # Correlations
        self.story.append(Paragraph("🔗 Zidentyfikowane korelacje:", self.styles['Subsection']))
        for i, corr in enumerate(forecast.identified_correlations, 1):
            self.story.append(Paragraph(f"<b>{i}. Korelacja między:</b>", self.styles['IndentedText']))
            self.story.append(Paragraph(f"• {corr.fact_1}", self.styles['IndentedText']))
            self.story.append(Paragraph(f"• {corr.fact_2}", self.styles['IndentedText']))
            self.story.append(Paragraph(f"→ <i>{corr.correlation_description}</i>", self.styles['IndentedText']))
            self.story.append(Paragraph(f"⚡ <b>Istotność:</b> {corr.relevance_to_forecast}", self.styles['IndentedText']))
            self.story.append(Spacer(1, 6))
        self.story.append(Spacer(1, 12))
        
        # Non-obvious factors
        self.story.append(Paragraph("🦢 Nieoczywiste czynniki (Deep Research):", self.styles['Subsection']))
        for i, factor in enumerate(forecast.non_obvious_factors, 1):
            self.story.append(Paragraph(f"<b>{i}. {factor.factor_name}</b>", self.styles['IndentedText']))
            self.story.append(Paragraph(f"• Opis: {factor.description}", self.styles['IndentedText']))
            self.story.append(Paragraph(f"• Potencjalny wpływ: {factor.potential_impact}", self.styles['IndentedText']))
            self.story.append(Spacer(1, 6))
        self.story.append(Spacer(1, 12))
        
        # Chain of reasoning
        self.story.append(Paragraph("🎯 Łańcuch rozumowania (krok po kroku):", self.styles['Subsection']))
        for step in forecast.chain_of_thought:
            self.story.append(Paragraph(
                f"<b>Krok {step.step_number}:</b> {step.description}",
                self.styles['IndentedText']
            ))
            self.story.append(Paragraph(
                f"→ Uzasadnienie: <i>{step.reasoning}</i>",
                self.styles['IndentedText']
            ))
            self.story.append(Spacer(1, 6))
        self.story.append(Spacer(1, 20))
        
        # Forecasts section
        self.story.append(Paragraph(
            f"📊 PROGNOZY (Pewność: {forecast.confidence:.2f})",
            self.styles['SectionHeader']
        ))
        
        # Create table for forecasts
        forecast_data = [
            ['Typ', 'Scenariusz'],
            ['✅ Pozytywny 1', forecast.positive_forecast_1],
            ['✅ Pozytywny 2', forecast.positive_forecast_2],
            ['❌ Negatywny 1', forecast.negative_forecast_1],
            ['❌ Negatywny 2', forecast.negative_forecast_2],
        ]
        
        forecast_table = Table(forecast_data, colWidths=[1.5*inch, 5*inch])
        forecast_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        self.story.append(forecast_table)
        self.story.append(Spacer(1, 20))
        
        # Explanations section
        self.story.append(Paragraph("💡 WYJAŚNIENIA", self.styles['SectionHeader']))
        
        self.story.append(Paragraph(
            f"🎯 <b>Wyjaśnienie pewności prognozy ({forecast.confidence:.2f}):</b>",
            self.styles['Subsection']
        ))
        self.story.append(Paragraph(forecast.confidence_explanation, self.styles['BodyJustify']))
        self.story.append(Spacer(1, 12))
        
        self.story.append(Paragraph("💭 <b>Uzasadnienie:</b>", self.styles['Subsection']))
        self.story.append(Paragraph(forecast.reasoning, self.styles['BodyJustify']))
        self.story.append(Spacer(1, 12))
        
        self.story.append(Paragraph("🔗 <b>Łańcuch przyczynowo-skutkowy:</b>", self.styles['Subsection']))
        self.story.append(Paragraph(forecast.causality, self.styles['BodyJustify']))
        self.story.append(Spacer(1, 20))
    
    def build(self):
        """Build the PDF document"""
        try:
            self.doc.build(self.story)
            logger.info(f"PDF report generated successfully: {self.output_path}")
            return self.output_path
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise
    
    def generate_report(self, scenario: dict, forecasts: List[dict], timestamp: datetime):
        """
        Generate complete PDF report with all country forecasts
        
        Args:
            scenario: Dictionary with scenario description and total_weight
            forecasts: List of dictionaries with country_name and forecast data
            timestamp: Timestamp for the report
        """
        # Add title page
        self.add_title_page(
            title="Raport Analiz Geopolitycznych",
            subtitle=f"Prognozy dla {len(forecasts)} krajów",
            scenario=scenario.get('description', '')
        )
        
        # Add each country's forecast
        scenario_weight = scenario.get('total_weight', 100)
        for forecast_data in forecasts:
            self.add_country_forecast(
                country_name=forecast_data['country_name'],
                forecasts=forecast_data['forecast'],
                scenario_weight=scenario_weight
            )
        
        # Build the PDF
        return self.build()
