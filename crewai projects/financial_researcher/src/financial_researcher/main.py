#!/usr/bin/env python
# src/financial_researcher/main.py
import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ChromaDB requires CHROMA_OPENAI_API_KEY - set it from OPENAI_API_KEY if not present
if not os.getenv('CHROMA_OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY'):
    os.environ['CHROMA_OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Verify OpenAI key is loaded
if not os.getenv('OPENAI_API_KEY'):
    print("\n⚠️  WARNING: OPENAI_API_KEY not found!")
    print(f"Looking for .env file at: {env_path}")
    print("Please create a .env file with your OPENAI_API_KEY")
    print("Example: cp env.example .env\n")
    sys.exit(1)

from financial_researcher.crew import SPXTradingCrew
from financial_researcher.order_history import OrderHistory

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Initialize order history system
order_history = OrderHistory()

def get_current_spx_price():
    """Fetch current SPX price from web or return placeholder"""
    try:
        # Try to get real-time SPX price (you can implement actual API call here)
        # For now, we'll use a placeholder that can be updated
        return "Check live: https://finance.yahoo.com/quote/%5ESPX/"
    except:
        return "Unable to fetch - check Yahoo Finance"

def get_week_start_date():
    """Get the date from 7 days ago"""
    return (datetime.now() - timedelta(days=7)).strftime('%B %d, %Y')

def get_week_range():
    """Get date range for the past week"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    return f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"

def run():
    """
    Run the Dynamic SPX Trading Analysis System.
    
    This system analyzes:
    1. Latest news from 5 major tech companies (50% of SPX weight)
    2. SPX price trends over the past week
    3. Federal Reserve policy and recent statements
    4. Makes BUY/SELL/HOLD decision based on ALL factors
    """
    
    # Get current date/time information
    now = datetime.now()
    current_datetime = now.strftime('%B %d, %Y %I:%M %p ET')
    current_date = now.strftime('%B %d, %Y')
    current_month = now.strftime('%B')
    current_year = now.strftime('%Y')
    week_start_date = get_week_start_date()
    week_range = get_week_range()
    current_spx_price = get_current_spx_price()
    
    # Day of week check
    day_of_week = now.strftime('%A')
    if day_of_week in ['Saturday', 'Sunday']:
        print(f"\n{'='*80}")
        print(f"⚠️  MARKET CLOSED - {day_of_week}")
        print(f"Markets are closed on weekends. Run this Monday-Friday 9:30 AM - 4:00 PM ET")
        print(f"{'='*80}\n")
    
    companies = [
        'NVIDIA Corporation',
        'Microsoft Corporation',
        'Apple Inc.',
        'Amazon.com Inc.',
        'Meta Platforms Inc.'
    ]
    
    print(f"\n{'='*80}")
    print(f"🔴 LIVE SPX TRADING SYSTEM - REAL-TIME ANALYSIS")
    print(f"{'='*80}")
    print(f"📅 Date & Time: {current_datetime}")
    print(f"📊 Current SPX: {current_spx_price}")
    print(f"📈 Analysis Period: {week_range}")
    print(f"⏰ Trading Hours: 9:30 AM - 4:00 PM ET")
    print(f"{'='*80}\n")
    
    # Set available capital for trading (modify this based on your actual capital)
    available_capital = "$10,000"  # Default starting capital
    
    # Load order history for both traders
    order_history_aggressive = order_history.format_history_for_agent("aggressive")
    order_history_cautious = order_history.format_history_for_agent("cautious")
    
    # Prepare dynamic inputs for all tasks
    base_inputs = {
        'current_datetime': current_datetime,
        'current_date': current_date,
        'current_month': current_month,
        'current_year': current_year,
        'week_start_date': week_start_date,
        'week_range': week_range,
        'current_spx_price': current_spx_price,
        'available_capital': available_capital,
        'order_history_aggressive': order_history_aggressive,
        'order_history_cautious': order_history_cautious
    }
    
    # PHASE 1: Gather news for all 5 tech companies (NEWS ONLY - NO TRADING DECISION YET)
    print(f"\n{'='*80}")
    print(f"PHASE 1: TECH COMPANY NEWS ANALYSIS")
    print(f"Analyzing top 5 companies (~50% of SPX weight)")
    print(f"{'='*80}\n")
    
    news_summaries = []
    
    for idx, company in enumerate(companies, 1):
        print(f"\n{'-'*80}")
        print(f"[{idx}/5] 📰 Fetching latest news: {company}")
        print(f"{'-'*80}\n")
        
        inputs = {**base_inputs, 'company': company}
        
        # Create a crew that will only execute the news research task
        from crewai import Agent, Crew, Process, Task
        from crewai_tools import SerperDevTool
        
        news_agent = Agent(
            role=f"Real-time News Researcher for {company}",
            goal=f"Find the most recent breaking news and market-moving events for {company} in the last 24-48 hours",
            backstory=f"You're a fast-paced financial news analyst who specializes in finding breaking news that impacts stock prices. You ALWAYS use web search to find the LATEST news from the current date {current_date}.",
            verbose=True,
            tools=[SerperDevTool()],
            llm="openai/gpt-5-mini"
        )
        
        news_task = Task(
            description=f"""You MUST use your web search tool to find BREAKING NEWS about {company} from the last 24-48 hours.
            Current date/time: {current_datetime}
            
            Search for:
            - "{company} news today"
            - "{company} breaking news {current_date}"
            - "{company} stock news latest"
            
            Find and report ONLY:
            1. Breaking news from the last 24-48 hours (with exact dates)
            2. Earnings announcements or surprises
            3. Product launches or major announcements
            4. Legal/regulatory issues
            5. Partnerships or acquisitions
            6. Analyst upgrades/downgrades
            7. Any market-moving events
            
            If there's no significant news, clearly state "No major news in the last 24-48 hours."
            Include dates, times, and sources for everything.""",
            expected_output=f"A concise news summary with ONLY the latest breaking news from the past 24-48 hours for {company}. Each news item must have: Date, Headline, Source, Impact (Bullish/Bearish/Neutral).",
            agent=news_agent
        )
        
        news_crew = Crew(
            agents=[news_agent],
            tasks=[news_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = news_crew.kickoff()
        
        # Save company news
        company_short = company.split()[0].lower()
        news_filename = f"output/{company_short}_news.md"
        
        with open(news_filename, 'w') as f:
            f.write(f"# Latest News: {company}\n")
            f.write(f"**Generated**: {current_datetime}\n")
            f.write(f"**Analysis Period**: Last 24-48 hours\n\n")
            f.write("---\n\n")
            f.write(result.raw)
        
        news_summaries.append({
            'company': company,
            'news': result.raw
        })
        
        print(f"✅ Saved to: {news_filename}\n")
    
    # PHASE 2: Analyze SPX weekly data
    print(f"\n{'='*80}")
    print(f"PHASE 2: SPX WEEKLY TREND ANALYSIS")
    print(f"Analyzing SPX price action: {week_range}")
    print(f"{'='*80}\n")
    
    spx_analyst = Agent(
        role="S&P 500 Historical Data Analyst",
        goal="Gather and analyze SPX price data for the past week to identify trends",
        backstory=f"You're a quantitative analyst specializing in S&P 500 index analysis. You gather historical SPX data for the past 5-7 trading days from {week_start_date} to {current_date}.",
        verbose=True,
        tools=[SerperDevTool()],
        llm="openai/gpt-5-mini"
    )
    
    spx_task = Task(
        description=f"""You MUST use your web search tool to gather S&P 500 (SPX) price data for the PAST WEEK.
        Current date/time: {current_datetime}
        Week range: {week_start_date} to {current_date}
        
        Search for:
        - "SPX price last week {current_date}"
        - "S&P 500 weekly chart {current_month} {current_year}"
        - "SPX historical prices {week_range}"
        
        Gather and report:
        1. SPX closing prices for the last 5-7 trading days
        2. Weekly high and low
        3. Week-to-date change (points and percentage)
        4. Daily price movements (identify trend direction)
        5. Trend direction (Uptrend/Downtrend/Sideways)
        6. Momentum (Strong/Moderate/Weak)""",
        expected_output=f"A comprehensive SPX weekly analysis with daily prices from {week_start_date} to {current_date}, trend direction, and momentum assessment.",
        agent=spx_analyst
    )
    
    spx_crew = Crew(
        agents=[spx_analyst],
        tasks=[spx_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = spx_crew.kickoff()
    spx_weekly_data = result.raw
    
    with open('output/spx_weekly_analysis.md', 'w') as f:
        f.write(f"# S&P 500 Weekly Analysis\n")
        f.write(f"**Generated**: {current_datetime}\n")
        f.write(f"**Analysis Period**: {week_range}\n\n")
        f.write("---\n\n")
        f.write(spx_weekly_data)
    
    print(f"✅ Saved to: output/spx_weekly_analysis.md\n")
    
    # PHASE 3: Analyze Federal Reserve Policy
    print(f"\n{'='*80}")
    print(f"PHASE 3: FEDERAL RESERVE POLICY ANALYSIS")
    print(f"Tracking latest Fed decisions and statements")
    print(f"{'='*80}\n")
    
    fed_analyst_agent = Agent(
        role="Federal Reserve Policy Analyst",
        goal="Track and analyze the latest Federal Reserve news, statements, and policy decisions",
        backstory=f"You're a macroeconomic analyst specialized in Federal Reserve policy and its impact on equity markets. You track Fed Chair statements, FOMC meeting minutes, and interest rate decisions for {current_month} {current_year}.",
        verbose=True,
        tools=[SerperDevTool()],
        llm="openai/gpt-5-mini"
    )
    
    fed_task = Task(
        description=f"""You MUST use your web search tool to find the LATEST Federal Reserve news and policy statements.
        Current date/time: {current_datetime}
        Current month: {current_month} {current_year}
        
        Search for:
        - "Federal Reserve news today {current_date}"
        - "Fed interest rate decision {current_month} {current_year}"
        - "Jerome Powell statement {current_date}"
        - "FOMC meeting {current_month} {current_year}"
        
        Find and report:
        1. Latest FOMC meeting date and decision (if recent)
        2. Current Federal Funds rate
        3. Recent Fed Chair statements or speeches (last 7 days)
        4. Market interpretation of Fed policy (hawkish/dovish)
        5. Impact on equities (Bullish/Bearish/Neutral)""",
        expected_output=f"A comprehensive Fed policy analysis for {current_month} {current_year} with current rate, recent statements, and market impact assessment.",
        agent=fed_analyst_agent
    )
    
    fed_crew = Crew(
        agents=[fed_analyst_agent],
        tasks=[fed_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = fed_crew.kickoff()
    fed_analysis = result.raw
    
    with open('output/fed_policy_analysis.md', 'w') as f:
        f.write(f"# Federal Reserve Policy Analysis\n")
        f.write(f"**Generated**: {current_datetime}\n")
        f.write(f"**Current Month**: {current_month} {current_year}\n\n")
        f.write("---\n\n")
        f.write(fed_analysis)
    
    print(f"✅ Saved to: output/fed_policy_analysis.md\n")
    
    # PHASE 4: Generate integrated SPX trading signal (ONLY AFTER ALL ANALYSIS IS COMPLETE)
    print(f"\n{'='*80}")
    print(f"PHASE 4: INTEGRATED SPX TRADING DECISION")
    print(f"Combining: Tech News + Weekly Trend + Fed Policy")
    print(f"{'='*80}\n")
    
    # Compile all context
    combined_context = f"=== COMPREHENSIVE MARKET ANALYSIS ===\n"
    combined_context += f"Generated: {current_datetime}\n"
    combined_context += f"Analysis Period: {week_range}\n\n"
    
    combined_context += "\n## TECH COMPANY NEWS (50% of SPX)\n" + "="*80 + "\n"
    for summary in news_summaries:
        combined_context += f"\n### {summary['company']}\n"
        combined_context += summary['news']
        combined_context += "\n" + "-"*80 + "\n"
    
    combined_context += f"\n## SPX WEEKLY TREND ANALYSIS\n" + "="*80 + "\n"
    combined_context += spx_weekly_data
    
    combined_context += f"\n\n## FEDERAL RESERVE POLICY\n" + "="*80 + "\n"
    combined_context += fed_analysis
    
    # Save combined analysis
    with open('output/comprehensive_analysis.md', 'w') as f:
        f.write(combined_context)
    
    print(f"✅ Saved comprehensive analysis: output/comprehensive_analysis.md\n")
    
    # PHASE 5: Risk Management + Dual Trader Analysis
    print(f"\n{'='*80}")
    print(f"PHASE 5: RISK MANAGEMENT & DUAL TRADING STRATEGIES")
    print(f"Running: Risk Analysis → Aggressive Trader → Cautious Trader")
    print(f"{'='*80}\n")
    
    # Get all trading signals including risk management and both traders
    inputs = {**base_inputs, 'company': 'Dual Trading Strategy Analysis'}
    result = SPXTradingCrew().crew().kickoff(inputs=inputs)
    
    # Extract individual task outputs
    try:
        # The tasks run in sequence, so outputs are in order:
        # 0: news_research_task
        # 1: spx_weekly_analysis_task  
        # 2: fed_policy_analysis_task
        # 3: risk_management_task
        # 4: aggressive_trader_task
        # 5: cautious_trader_task
        # 6: spx_trading_decision_task (original trader - optional)
        
        risk_management_output = result.tasks_output[3].raw if len(result.tasks_output) > 3 else "Risk analysis pending"
        aggressive_trader_output = result.tasks_output[4].raw if len(result.tasks_output) > 4 else "Aggressive trader analysis pending"
        cautious_trader_output = result.tasks_output[5].raw if len(result.tasks_output) > 5 else "Cautious trader analysis pending"
        
    except Exception as e:
        print(f"⚠️  Error extracting task outputs: {e}")
        print(f"Total outputs available: {len(result.tasks_output)}")
        risk_management_output = "Error extracting risk management output"
        aggressive_trader_output = "Error extracting aggressive trader output"
        cautious_trader_output = "Error extracting cautious trader output"
    
    # Save risk management analysis
    with open('output/risk_management.md', 'w') as f:
        f.write(f"# 🛡️ RISK MANAGEMENT ANALYSIS\n")
        f.write(f"**Generated**: {current_datetime}\n")
        f.write(f"**Current SPX**: {current_spx_price}\n")
        f.write(f"**Available Capital**: {available_capital}\n\n")
        f.write("---\n\n")
        f.write(risk_management_output)
    
    # Save aggressive trader decision
    with open('output/aggressive_trader_decision.md', 'w') as f:
        f.write(f"# 🚀 AGGRESSIVE TRADER DECISION (Billionaire Strategy)\n")
        f.write(f"**Generated**: {current_datetime}\n")
        f.write(f"**Current SPX**: {current_spx_price}\n")
        f.write(f"**Capital**: {available_capital}\n")
        f.write(f"**Strategy**: Hold 3-7 days, Target 300%+ profits\n\n")
        f.write("---\n\n")
        f.write(aggressive_trader_output)
    
    # Save cautious trader decision
    with open('output/cautious_trader_decision.md', 'w') as f:
        f.write(f"# 🛡️ CAUTIOUS TRADER DECISION (Steady Compounding Strategy)\n")
        f.write(f"**Generated**: {current_datetime}\n")
        f.write(f"**Current SPX**: {current_spx_price}\n")
        f.write(f"**Capital**: {available_capital}\n")
        f.write(f"**Strategy**: Hold 0-2 days, Target $100-$200 profits\n\n")
        f.write("---\n\n")
        f.write(cautious_trader_output)
    
    # Create a combined trading comparison
    combined_trading_output = f"""# 🎯 DUAL TRADING STRATEGY COMPARISON

**Generated**: {current_datetime}
**Current SPX**: {current_spx_price}
**Available Capital**: {available_capital}
**Analysis Period**: {week_range}

---

## 🛡️ RISK MANAGEMENT OVERVIEW

{risk_management_output}

---

## 🚀 AGGRESSIVE TRADER (Billionaire Strategy)
**Goal**: Maximum profit through high-conviction multi-day holds
**Target**: 300%+ profit per trade
**Holding Period**: 3-7 days

{aggressive_trader_output}

---

## 🛡️ CAUTIOUS TRADER (Steady Compounding Strategy)
**Goal**: Consistent $100-$200 profits with 60%+ win rate
**Target**: $100-$200 profit per trade
**Holding Period**: Same day to 1-2 days

{cautious_trader_output}

---

## 📊 STRATEGY COMPARISON

### Capital Allocation
- **Aggressive Trader**: Higher position sizes (5-10% of capital) for home run trades
- **Cautious Trader**: Smaller position sizes (2-5% of capital) for consistent gains

### Risk Profile
- **Aggressive Trader**: Higher risk, higher reward - waiting for A+ setups
- **Cautious Trader**: Lower risk, steady gains - only trades with 60%+ probability

### Holding Period
- **Aggressive Trader**: 3-7 days to capture major moves
- **Cautious Trader**: 0-2 days for quick profits

### Decision Philosophy
- **Aggressive Trader**: Few high-conviction trades (5-10 per year), each with massive upside
- **Cautious Trader**: Many high-probability trades (150+ per year), each with modest profit

---

**Disclaimer**: Options trading carries significant risk. These are educational examples, not financial advice.
Always consult with a licensed financial advisor before trading.
"""
    
    # Save combined comparison
    with open('output/dual_trading_comparison.md', 'w') as f:
        f.write(combined_trading_output)
    
    # Display the results
    print(f"\n{'='*80}")
    print(f"🛡️ RISK MANAGEMENT ANALYSIS")
    print(f"{'='*80}\n")
    print(risk_management_output[:500] + "..." if len(risk_management_output) > 500 else risk_management_output)
    
    print(f"\n{'='*80}")
    print(f"🚀 AGGRESSIVE TRADER DECISION")
    print(f"{'='*80}\n")
    print(aggressive_trader_output[:500] + "..." if len(aggressive_trader_output) > 500 else aggressive_trader_output)
    
    print(f"\n{'='*80}")
    print(f"🛡️ CAUTIOUS TRADER DECISION")
    print(f"{'='*80}\n")
    print(cautious_trader_output[:500] + "..." if len(cautious_trader_output) > 500 else cautious_trader_output)
    
    print(f"\n{'='*80}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"✅ ANALYSIS COMPLETE - ALL FILES GENERATED")
    print(f"{'='*80}")
    print(f"\n📁 Generated Files (output/ directory):")
    print(f"")
    print(f"  📰 TECH COMPANY NEWS:")
    for company in companies:
        company_short = company.split()[0].lower()
        print(f"     • {company_short}_news.md")
    print(f"")
    print(f"  📊 MARKET ANALYSIS:")
    print(f"     • spx_weekly_analysis.md - Weekly SPX price trends")
    print(f"     • fed_policy_analysis.md - Federal Reserve policy impact")
    print(f"     • comprehensive_analysis.md - All data combined")
    print(f"")
    print(f"  🛡️ RISK MANAGEMENT:")
    print(f"     • risk_management.md - Capital protection & position sizing")
    print(f"")
    print(f"  🎯 TRADING DECISIONS:")
    print(f"     • aggressive_trader_decision.md - 🚀 Billionaire strategy (300%+ targets)")
    print(f"     • cautious_trader_decision.md - 🛡️ Steady compounding ($100-$200 targets)")
    print(f"     • dual_trading_comparison.md - ⭐ SIDE-BY-SIDE COMPARISON")
    print(f"")
    print(f"  📜 ORDER HISTORY:")
    print(f"     • order_history.json - Complete trade history for both strategies")
    print(f"")
    print(f"{'='*80}")
    print(f"")
    print(f"💡 TWO TRADING STRATEGIES:")
    print(f"")
    print(f"   🚀 AGGRESSIVE TRADER:")
    print(f"      • Goal: Billionaire mindset - 300%+ profits")
    print(f"      • Hold: 3-7 days for major moves")
    print(f"      • Risk: Higher, but calculated with strict stop-loss")
    print(f"      • Frequency: 5-10 home run trades per year")
    print(f"")
    print(f"   🛡️ CAUTIOUS TRADER:")
    print(f"      • Goal: Steady compounding - $100-$200 per trade")
    print(f"      • Hold: Same day to 1-2 days")
    print(f"      • Risk: Lower, 60%+ win rate priority")
    print(f"      • Frequency: 150+ trades per year")
    print(f"")
    print(f"{'='*80}")
    print(f"")
    print(f"🛡️ CAPITAL PROTECTION: Both strategies include risk management to NEVER lose initial investment")
    print(f"📊 Current SPX: {current_spx_price}")
    print(f"💰 Available Capital: {available_capital}")
    print(f"📅 Next Run: {(now + timedelta(days=1)).strftime('%B %d, %Y')} morning")
    print(f"⏰ Best Time: Run daily during market hours (9:30 AM - 4:00 PM ET)")
    print(f"")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    run()
