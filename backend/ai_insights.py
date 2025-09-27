"""
AI-Driven Insights and Pattern Recognition for StockWise
Provides intelligent analysis of batch scan results using LLM integration
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class StockInsightsAI:
    """AI-powered stock analysis and pattern recognition"""
    
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            logger.warning("EMERGENT_LLM_KEY not found in environment")
        
        self.system_message = """You are a professional stock market analyst and pattern recognition expert. 
        Your role is to analyze batch scan results and provide intelligent insights about:
        
        1. Market trends and patterns
        2. Sector performance analysis  
        3. Technical indicator insights
        4. Risk assessment and opportunities
        5. Actionable recommendations for traders
        
        Always provide clear, concise, and actionable insights. Focus on practical trading implications.
        Use professional financial terminology and back your analysis with data from the results provided."""
    
    async def analyze_batch_results(self, batch_results: List[Dict[str, Any]], 
                                  scan_filters: Dict[str, Any], 
                                  scan_indices: List[str]) -> Dict[str, Any]:
        """
        Analyze batch scan results and generate AI-driven insights
        
        Args:
            batch_results: List of stock data from batch scan
            scan_filters: Filters used in the batch scan
            scan_indices: Stock indices that were scanned
            
        Returns:
            Dictionary containing AI insights and recommendations
        """
        if not self.api_key or not batch_results:
            return self._generate_fallback_analysis(batch_results, scan_filters, scan_indices)
        
        try:
            # Prepare analysis data
            analysis_data = self._prepare_analysis_data(batch_results, scan_filters, scan_indices)
            
            # Create AI chat session
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                system_message=self.system_message
            ).with_model("openai", "gpt-4o-mini")
            
            # Create analysis prompt
            analysis_prompt = self._create_analysis_prompt(analysis_data)
            
            # Send to AI for analysis
            user_message = UserMessage(text=analysis_prompt)
            ai_response = await chat.send_message(user_message)
            
            # Process and structure the response
            insights = self._process_ai_response(ai_response, batch_results)
            
            logger.info(f"AI analysis completed for {len(batch_results)} stocks")
            return insights
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._generate_fallback_analysis(batch_results, scan_filters, scan_indices)
    
    def _prepare_analysis_data(self, batch_results: List[Dict[str, Any]], 
                             scan_filters: Dict[str, Any], 
                             scan_indices: List[str]) -> Dict[str, Any]:
        """Prepare structured data for AI analysis"""
        
        # Calculate summary statistics
        total_stocks = len(batch_results)
        avg_price = sum(stock.get('price', 0) for stock in batch_results) / total_stocks if total_stocks > 0 else 0
        
        # Sector distribution
        sectors = {}
        for stock in batch_results:
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        # PPO patterns analysis
        ppo_patterns = {
            'positive_hooks': len([s for s in batch_results if s.get('ppo_hook_type') == 'positive']),
            'negative_hooks': len([s for s in batch_results if s.get('ppo_hook_type') == 'negative']),
            'high_slope': len([s for s in batch_results if s.get('ppo_slope_percentage', 0) > 10])
        }
        
        # Volume analysis
        high_volume_stocks = [s for s in batch_results if s.get('volume_today', 0) > s.get('volume_3m', 0) * 1.5]
        
        # Top performers by different metrics
        top_by_slope = sorted(batch_results, key=lambda x: x.get('ppo_slope_percentage', 0), reverse=True)[:5]
        top_by_dmi = sorted(batch_results, key=lambda x: x.get('dmi', 0), reverse=True)[:5]
        
        return {
            'scan_summary': {
                'total_stocks': total_stocks,
                'avg_price': avg_price,
                'indices_scanned': scan_indices,
                'filters_applied': scan_filters
            },
            'sector_distribution': sectors,
            'technical_patterns': ppo_patterns,
            'volume_analysis': {
                'high_volume_count': len(high_volume_stocks),
                'high_volume_stocks': [s['symbol'] for s in high_volume_stocks[:10]]
            },
            'top_performers': {
                'by_ppo_slope': [{'symbol': s['symbol'], 'slope': s.get('ppo_slope_percentage', 0)} for s in top_by_slope],
                'by_dmi': [{'symbol': s['symbol'], 'dmi': s.get('dmi', 0)} for s in top_by_dmi]
            }
        }
    
    def _create_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Create a structured prompt for AI analysis"""
        
        prompt = f"""
        Analyze the following stock batch scan results and provide professional insights:

        ## SCAN SUMMARY
        - Total stocks analyzed: {analysis_data['scan_summary']['total_stocks']}
        - Average price: ${analysis_data['scan_summary']['avg_price']:.2f}
        - Indices scanned: {', '.join(analysis_data['scan_summary']['indices_scanned'])}
        - Filters applied: {json.dumps(analysis_data['scan_summary']['filters_applied'], indent=2)}

        ## SECTOR DISTRIBUTION
        {json.dumps(analysis_data['sector_distribution'], indent=2)}

        ## TECHNICAL PATTERNS
        - Positive PPO hooks: {analysis_data['technical_patterns']['positive_hooks']}
        - Negative PPO hooks: {analysis_data['technical_patterns']['negative_hooks']}
        - High PPO slope (>10%): {analysis_data['technical_patterns']['high_slope']}

        ## VOLUME ANALYSIS
        - High volume stocks (>1.5x avg): {analysis_data['volume_analysis']['high_volume_count']}
        - Notable symbols: {', '.join(analysis_data['volume_analysis']['high_volume_stocks'])}

        ## TOP PERFORMERS
        By PPO Slope: {json.dumps(analysis_data['top_performers']['by_ppo_slope'], indent=2)}
        By DMI: {json.dumps(analysis_data['top_performers']['by_dmi'], indent=2)}

        Please provide:
        1. **Market Sentiment Analysis**: What does this data suggest about current market conditions?
        2. **Sector Insights**: Which sectors are showing strength/weakness and why?
        3. **Technical Pattern Analysis**: What do the PPO hooks and DMI readings indicate?
        4. **Volume Insights**: What does the volume activity suggest about institutional interest?
        5. **Top Recommendations**: Which 3-5 stocks deserve immediate attention and why?
        6. **Risk Assessment**: What are the key risks and opportunities in this scan?
        
        Keep responses concise but actionable. Focus on practical trading implications.
        """
        
        return prompt
    
    def _process_ai_response(self, ai_response: str, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and structure the AI response into actionable insights"""
        
        # Extract key metrics for validation
        total_results = len(batch_results)
        avg_price = sum(stock.get('price', 0) for stock in batch_results) / total_results if total_results > 0 else 0
        
        return {
            'ai_analysis': ai_response,
            'analysis_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'gpt-4o-mini',
                'stocks_analyzed': total_results,
                'avg_stock_price': round(avg_price, 2)
            },
            'key_insights': self._extract_key_insights(ai_response),
            'recommendations': self._extract_recommendations(ai_response),
            'risk_factors': self._extract_risk_factors(ai_response)
        }
    
    def _extract_key_insights(self, ai_response: str) -> List[str]:
        """Extract key insights from AI response with improved parsing"""
        insights = []
        lines = ai_response.split('\n')
        
        # Look for sections with insights
        in_insights_section = False
        in_recommendations_section = False
        
        for line in lines:
            line_clean = line.strip()
            
            # Detect section headers
            if any(keyword in line_clean.lower() for keyword in ['market sentiment', 'key insight', 'finding', 'analysis']):
                in_insights_section = True
                continue
            elif any(keyword in line_clean.lower() for keyword in ['recommendation', 'suggestion']):
                in_insights_section = False
                in_recommendations_section = True
                continue
            elif line_clean.startswith('##') or line_clean.startswith('**'):
                in_insights_section = False
                in_recommendations_section = False
                continue
            
            # Extract insights from relevant sections
            if in_insights_section and line_clean:
                if (line_clean.startswith('1.') or line_clean.startswith('2.') or 
                    line_clean.startswith('3.') or line_clean.startswith('4.') or 
                    line_clean.startswith('5.') or line_clean.startswith('-') or
                    line_clean.startswith('*') or line_clean.startswith('•')):
                    
                    # Clean up the text
                    clean_insight = line_clean.lstrip('123456789.-*•').strip()
                    if len(clean_insight) > 10:  # Ignore very short entries
                        insights.append(clean_insight)
                elif len(line_clean) > 20 and not line_clean.startswith('#'):
                    # Include longer descriptive lines
                    insights.append(line_clean)
        
        # If no insights found, extract from the entire response
        if not insights:
            for line in lines:
                line_clean = line.strip()
                if (line_clean and not line_clean.startswith('#') and 
                    len(line_clean) > 15 and 
                    any(keyword in line_clean.lower() for keyword in 
                        ['stock', 'market', 'trend', 'momentum', 'volume', 'price', 'sector'])):
                    insights.append(line_clean)
        
        return insights[:10]  # Limit to top 10 insights
    
    def _extract_recommendations(self, ai_response: str) -> List[str]:
        """Extract specific stock recommendations with improved parsing"""
        recommendations = []
        lines = ai_response.split('\n')
        
        # Look for recommendation sections
        in_recommendations = False
        in_top_performers = False
        
        for line in lines:
            line_clean = line.strip()
            
            # Detect recommendation sections
            if any(keyword in line_clean.lower() for keyword in 
                  ['recommendation', 'top', 'attention', 'buy', 'watch', 'focus']):
                in_recommendations = True
                continue
            elif any(keyword in line_clean.lower() for keyword in 
                    ['risk', 'caution', 'technical', 'appendix']):
                in_recommendations = False
                continue
            
            # Extract recommendations
            if in_recommendations and line_clean:
                if (line_clean.startswith(('1.', '2.', '3.', '4.', '5.')) or
                    line_clean.startswith('-') or line_clean.startswith('•') or
                    any(word in line_clean.upper() for word in 
                        ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NEE', 'MO', 'ORCL'])):
                    
                    # Clean recommendation text
                    clean_rec = line_clean.lstrip('123456789.-*•').strip()
                    if len(clean_rec) > 5:
                        recommendations.append(clean_rec)
                elif (len(line_clean) > 20 and 
                      any(keyword in line_clean.lower() for keyword in 
                          ['should', 'consider', 'focus', 'attention', 'strong', 'potential'])):
                    recommendations.append(line_clean)
        
        # If no recommendations found, look for stock symbols with context
        if not recommendations:
            for line in lines:
                line_clean = line.strip()
                if any(symbol in line_clean.upper() for symbol in 
                      ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'UNH', 'JNJ', 'WMT', 'PG']):
                    if len(line_clean) > 10:
                        recommendations.append(line_clean)
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _extract_risk_factors(self, ai_response: str) -> List[str]:
        """Extract risk factors with improved parsing"""
        risks = []
        lines = ai_response.split('\n')
        
        in_risk_section = False
        
        for line in lines:
            line_clean = line.strip()
            
            # Detect risk sections
            if any(keyword in line_clean.lower() for keyword in 
                  ['risk', 'caution', 'warning', 'concern', 'challenge']):
                in_risk_section = True
                if len(line_clean) > 10:  # If the header line itself contains risk info
                    risks.append(line_clean)
                continue
            elif any(keyword in line_clean.lower() for keyword in 
                    ['recommendation', 'technical', 'appendix']):
                in_risk_section = False
                continue
            
            # Extract risk content
            if in_risk_section and line_clean:
                if (line_clean.startswith(('1.', '2.', '3.', '4.', '5.')) or
                    line_clean.startswith('-') or line_clean.startswith('•') or
                    any(keyword in line_clean.lower() for keyword in 
                        ['low', 'high', 'limited', 'volatile', 'decline', 'pressure'])):
                    
                    clean_risk = line_clean.lstrip('123456789.-*•').strip()
                    if len(clean_risk) > 10:
                        risks.append(clean_risk)
                elif len(line_clean) > 15:
                    risks.append(line_clean)
        
        # Fallback: look for any risk-related content
        if not risks:
            for line in lines:
                line_clean = line.strip()
                if (len(line_clean) > 15 and 
                    any(keyword in line_clean.lower() for keyword in 
                        ['risk', 'concern', 'caution', 'volatility', 'decline', 'pressure', 'low volume'])):
                    risks.append(line_clean)
        
        return risks[:5]  # Limit to top 5 risks
    
    def _generate_fallback_analysis(self, batch_results: List[Dict[str, Any]], 
                                  scan_filters: Dict[str, Any], 
                                  scan_indices: List[str]) -> Dict[str, Any]:
        """Generate basic statistical analysis when AI is not available"""
        
        if not batch_results:
            return {
                'ai_analysis': 'No results to analyze',
                'analysis_metadata': {
                    'generated_at': datetime.utcnow().isoformat(),
                    'model_used': 'fallback_statistical',
                    'stocks_analyzed': 0
                }
            }
        
        total_results = len(batch_results)
        avg_price = sum(stock.get('price', 0) for stock in batch_results) / total_results
        
        # Basic statistical analysis
        high_dmi_stocks = [s for s in batch_results if s.get('dmi', 0) > 30]
        high_slope_stocks = [s for s in batch_results if s.get('ppo_slope_percentage', 0) > 10]
        
        fallback_analysis = f"""
        STATISTICAL ANALYSIS (AI unavailable)
        
        Scan Results Summary:
        - Total stocks analyzed: {total_results}
        - Average price: ${avg_price:.2f}
        - Indices: {', '.join(scan_indices)}
        
        Key Findings:
        - High DMI stocks (>30): {len(high_dmi_stocks)} ({len(high_dmi_stocks)/total_results*100:.1f}%)
        - High PPO slope stocks (>10%): {len(high_slope_stocks)} ({len(high_slope_stocks)/total_results*100:.1f}%)
        
        This is a basic statistical analysis. Enable AI for comprehensive insights.
        """
        
        return {
            'ai_analysis': fallback_analysis,
            'analysis_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'model_used': 'fallback_statistical',
                'stocks_analyzed': total_results,
                'avg_stock_price': round(avg_price, 2)
            },
            'key_insights': [
                f"Analyzed {total_results} stocks with average price ${avg_price:.2f}",
                f"{len(high_dmi_stocks)} stocks show high directional movement (DMI > 30)",
                f"{len(high_slope_stocks)} stocks have strong PPO momentum (slope > 10%)"
            ],
            'recommendations': ["Enable AI analysis for detailed recommendations"],
            'risk_factors': ["Statistical analysis only - limited insight depth"]
        }

# Import cache_manager for compatibility
from batch_cache import cache_manager

# Global instance
ai_insights = StockInsightsAI()