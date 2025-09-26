"""
Professional PDF Report Generator for StockWise AI Insights
Creates formatted PDF reports with charts, analysis, and recommendations
"""

import os
import io
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus import Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import logging

logger = logging.getLogger(__name__)

class AIInsightsPDFGenerator:
    """Professional PDF report generator for AI stock insights"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Create custom paragraph styles for the report"""
        
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Header style  
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold'
        )
        
        # Subheader style
        self.subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=15,
            textColor=colors.HexColor('#4b5563'),
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=3,
            textColor=colors.HexColor('#1f2937'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        # Insight item style
        self.insight_style = ParagraphStyle(
            'InsightItem',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            spaceBefore=2,
            leftIndent=20,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica'
        )
        
        # Metadata style
        self.metadata_style = ParagraphStyle(
            'MetadataStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica-Oblique'
        )
    
    async def generate_insights_pdf(self, 
                                  insights: Dict[str, Any], 
                                  batch_results: List[Dict[str, Any]], 
                                  batch_id: str,
                                  scan_filters: Dict[str, Any] = None,
                                  scan_indices: List[str] = None) -> bytes:
        """
        Generate comprehensive AI insights PDF report
        
        Args:
            insights: AI analysis results
            batch_results: Stock scan results
            batch_id: Batch job identifier
            scan_filters: Filters used in the scan
            scan_indices: Indices that were scanned
            
        Returns:
            PDF file as bytes
        """
        try:
            # Create PDF buffer
            buffer = io.BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build report content
            story = []
            
            # Title page
            story.extend(self._create_title_page(insights, batch_id, scan_indices))
            
            # Executive summary
            story.extend(self._create_executive_summary(insights, batch_results))
            
            # Market analysis charts
            chart_images = self._create_analysis_charts(batch_results, insights)
            story.extend(self._add_charts_section(chart_images))
            
            # Detailed AI analysis
            story.extend(self._create_detailed_analysis(insights))
            
            # Key insights and recommendations
            story.extend(self._create_insights_section(insights))
            
            # Risk assessment
            story.extend(self._create_risk_section(insights))
            
            # Technical appendix
            story.extend(self._create_technical_appendix(batch_results, scan_filters))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            buffer.seek(0)
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            # Clean up chart files
            self._cleanup_chart_files(chart_images)
            
            logger.info(f"Generated AI insights PDF report for batch {batch_id}: {len(pdf_bytes)} bytes")
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {e}")
            raise
    
    def _create_title_page(self, insights: Dict[str, Any], batch_id: str, scan_indices: List[str]) -> List:
        """Create the title page of the report"""
        content = []
        
        # Main title
        content.append(Paragraph("StockWise AI Insights Report", self.title_style))
        content.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = f"Professional Market Analysis & Pattern Recognition"
        content.append(Paragraph(subtitle, self.header_style))
        content.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        metadata = insights.get('analysis_metadata', {})
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        metadata_text = f"""
        <b>Report Generated:</b> {report_date}<br/>
        <b>Batch ID:</b> {batch_id}<br/>
        <b>Stocks Analyzed:</b> {metadata.get('stocks_analyzed', 'N/A')}<br/>
        <b>AI Model:</b> {metadata.get('model_used', 'GPT-4o-mini')}<br/>
        <b>Indices Scanned:</b> {', '.join(scan_indices) if scan_indices else 'Unknown'}<br/>
        <b>Average Stock Price:</b> ${metadata.get('avg_stock_price', 0):.2f}
        """
        
        content.append(Paragraph(metadata_text, self.body_style))
        content.append(Spacer(1, 1*inch))
        
        # Disclaimer
        disclaimer = """
        <b>Important Disclaimer:</b> This report is generated by artificial intelligence for informational 
        purposes only. It does not constitute financial advice, investment recommendations, or a solicitation 
        to buy or sell securities. Always consult with qualified financial professionals before making 
        investment decisions. Past performance does not guarantee future results.
        """
        content.append(Paragraph(disclaimer, self.metadata_style))
        
        content.append(PageBreak())
        return content
    
    def _create_executive_summary(self, insights: Dict[str, Any], batch_results: List[Dict[str, Any]]) -> List:
        """Create executive summary section"""
        content = []
        
        content.append(Paragraph("Executive Summary", self.header_style))
        
        # Key metrics
        total_stocks = len(batch_results)
        avg_price = sum(stock.get('price', 0) for stock in batch_results) / total_stocks if total_stocks > 0 else 0
        
        # PPO analysis
        positive_hooks = len([s for s in batch_results if s.get('ppo_hook_type') == 'positive'])
        high_slope_stocks = len([s for s in batch_results if s.get('ppo_slope_percentage', 0) > 10])
        
        summary_text = f"""
        This analysis covers {total_stocks} stocks with an average price of ${avg_price:.2f}. 
        The scan identified {positive_hooks} stocks with positive PPO hook patterns and 
        {high_slope_stocks} stocks with high momentum (PPO slope > 10%).
        """
        
        content.append(Paragraph(summary_text, self.body_style))
        content.append(Spacer(1, 0.2*inch))
        
        # Key highlights from AI analysis
        if insights.get('key_insights'):
            content.append(Paragraph("Key Market Highlights:", self.subheader_style))
            
            for i, insight in enumerate(insights['key_insights'][:5], 1):
                insight_text = f"• {insight}"
                content.append(Paragraph(insight_text, self.insight_style))
        
        content.append(Spacer(1, 0.3*inch))
        return content
    
    def _create_analysis_charts(self, batch_results: List[Dict[str, Any]], insights: Dict[str, Any]) -> Dict[str, str]:
        """Create analysis charts and return file paths"""
        chart_files = {}
        
        try:
            # Set style
            plt.style.use('seaborn-v0_8-whitegrid')
            
            # Chart 1: Price distribution
            if batch_results:
                fig, ax = plt.subplots(1, 1, figsize=(8, 5))
                prices = [stock.get('price', 0) for stock in batch_results if stock.get('price', 0) > 0]
                if prices:
                    ax.hist(prices, bins=20, alpha=0.7, color='#3b82f6', edgecolor='black')
                    ax.set_xlabel('Stock Price ($)')
                    ax.set_ylabel('Frequency')
                    ax.set_title('Stock Price Distribution')
                    ax.grid(True, alpha=0.3)
                    
                    price_chart_path = '/tmp/price_distribution.png'
                    plt.tight_layout()
                    plt.savefig(price_chart_path, dpi=300, bbox_inches='tight')
                    plt.close()
                    chart_files['price_distribution'] = price_chart_path
            
            # Chart 2: PPO Slope analysis
            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
            slopes = [stock.get('ppo_slope_percentage', 0) for stock in batch_results]
            if slopes:
                ax.scatter(range(len(slopes)), slopes, alpha=0.6, color='#10b981', s=30)
                ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)
                ax.axhline(y=10, color='orange', linestyle='--', alpha=0.7, label='High momentum threshold')
                ax.set_xlabel('Stock Index')
                ax.set_ylabel('PPO Slope Percentage (%)')
                ax.set_title('PPO Momentum Analysis')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                ppo_chart_path = '/tmp/ppo_analysis.png'
                plt.tight_layout()
                plt.savefig(ppo_chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                chart_files['ppo_analysis'] = ppo_chart_path
            
            # Chart 3: Sector distribution (if available)
            sectors = {}
            for stock in batch_results:
                sector = stock.get('sector', 'Unknown')
                sectors[sector] = sectors.get(sector, 0) + 1
            
            if len(sectors) > 1:
                fig, ax = plt.subplots(1, 1, figsize=(10, 6))
                sector_names = list(sectors.keys())
                sector_counts = list(sectors.values())
                
                colors_palette = plt.cm.Set3(range(len(sectors)))
                ax.pie(sector_counts, labels=sector_names, autopct='%1.1f%%', 
                      colors=colors_palette, startangle=90)
                ax.set_title('Sector Distribution')
                
                sector_chart_path = '/tmp/sector_distribution.png'
                plt.tight_layout()
                plt.savefig(sector_chart_path, dpi=300, bbox_inches='tight')
                plt.close()
                chart_files['sector_distribution'] = sector_chart_path
        
        except Exception as e:
            logger.warning(f"Failed to generate some charts: {e}")
        
        return chart_files
    
    def _add_charts_section(self, chart_files: Dict[str, str]) -> List:
        """Add charts section to the report"""
        content = []
        
        content.append(Paragraph("Market Analysis Charts", self.header_style))
        
        # Add charts
        for chart_name, chart_path in chart_files.items():
            if os.path.exists(chart_path):
                try:
                    # Chart title
                    chart_title = chart_name.replace('_', ' ').title()
                    content.append(Paragraph(chart_title, self.subheader_style))
                    
                    # Add chart image
                    img = Image(chart_path, width=6*inch, height=3.5*inch)
                    content.append(img)
                    content.append(Spacer(1, 0.3*inch))
                    
                except Exception as e:
                    logger.warning(f"Failed to add chart {chart_name}: {e}")
        
        content.append(PageBreak())
        return content
    
    def _create_detailed_analysis(self, insights: Dict[str, Any]) -> List:
        """Create detailed AI analysis section"""
        content = []
        
        content.append(Paragraph("Detailed AI Market Analysis", self.header_style))
        
        ai_analysis = insights.get('ai_analysis', 'No detailed analysis available.')
        
        # Split analysis into paragraphs for better formatting
        paragraphs = ai_analysis.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Clean up formatting
                clean_para = para.strip().replace('\n', ' ')
                content.append(Paragraph(clean_para, self.body_style))
                content.append(Spacer(1, 0.1*inch))
        
        content.append(Spacer(1, 0.2*inch))
        return content
    
    def _create_insights_section(self, insights: Dict[str, Any]) -> List:
        """Create key insights and recommendations section"""
        content = []
        
        # Key Insights
        if insights.get('key_insights'):
            content.append(Paragraph("Key Market Insights", self.header_style))
            
            for insight in insights['key_insights']:
                content.append(Paragraph(f"• {insight}", self.insight_style))
            
            content.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        if insights.get('recommendations'):
            content.append(Paragraph("Investment Recommendations", self.header_style))
            
            for i, rec in enumerate(insights['recommendations'], 1):
                rec_text = f"{i}. {rec}"
                content.append(Paragraph(rec_text, self.body_style))
                content.append(Spacer(1, 0.1*inch))
        
        return content
    
    def _create_risk_section(self, insights: Dict[str, Any]) -> List:
        """Create risk assessment section"""
        content = []
        
        if insights.get('risk_factors'):
            content.append(Paragraph("Risk Assessment", self.header_style))
            
            risk_intro = """
            The following risk factors have been identified based on the analysis of market 
            conditions, technical indicators, and current stock performance patterns:
            """
            content.append(Paragraph(risk_intro, self.body_style))
            content.append(Spacer(1, 0.2*inch))
            
            for i, risk in enumerate(insights['risk_factors'], 1):
                risk_text = f"<b>Risk {i}:</b> {risk}"
                content.append(Paragraph(risk_text, self.body_style))
                content.append(Spacer(1, 0.1*inch))
        
        content.append(PageBreak())
        return content
    
    def _create_technical_appendix(self, batch_results: List[Dict[str, Any]], scan_filters: Dict[str, Any]) -> List:
        """Create technical appendix with scan parameters"""
        content = []
        
        content.append(Paragraph("Technical Appendix", self.header_style))
        
        # Scan parameters
        content.append(Paragraph("Scan Parameters Used:", self.subheader_style))
        
        if scan_filters:
            filters_text = f"""
            <b>Price Filter:</b> {scan_filters.get('price_filter', 'Not specified')}<br/>
            <b>DMI Filter:</b> {scan_filters.get('dmi_filter', 'Not specified')}<br/>
            <b>PPO Slope Filter:</b> {scan_filters.get('ppo_slope_filter', 'Not specified')}<br/>
            <b>Hook Filter:</b> {scan_filters.get('ppo_hook_filter', 'All')}<br/>
            """
            content.append(Paragraph(filters_text, self.body_style))
        
        content.append(Spacer(1, 0.3*inch))
        
        # Technical indicators explanation
        content.append(Paragraph("Technical Indicators Explained:", self.subheader_style))
        
        indicators_text = """
        <b>PPO (Percentage Price Oscillator):</b> Momentum indicator showing the percentage 
        difference between two moving averages. Positive values suggest upward momentum.<br/><br/>
        
        <b>DMI (Directional Movement Index):</b> Measures the strength of price movement 
        direction. Higher values indicate stronger directional movement.<br/><br/>
        
        <b>PPO Slope:</b> Rate of change in PPO values, indicating acceleration or 
        deceleration of momentum. Always displayed as positive values in this analysis.<br/><br/>
        
        <b>Hook Patterns:</b> Specific PPO reversal patterns that may signal potential 
        trend changes or continuation patterns.
        """
        
        content.append(Paragraph(indicators_text, self.body_style))
        
        return content
    
    def _cleanup_chart_files(self, chart_files: Dict[str, str]):
        """Clean up temporary chart files"""
        for file_path in chart_files.values():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up chart file {file_path}: {e}")

# Global instance
pdf_generator = AIInsightsPDFGenerator()