# 🎯 Dynamic SPX Trading System - User Guide

## System Overview

This is a **real-time, year-round S&P 500 trading system** that automatically adapts to the current date and time. It provides BUY/SELL/HOLD recommendations based on three critical factors:

### 1. 📰 Tech Company News (50% of SPX Weight)
- NVIDIA Corporation (NVDA)
- Microsoft Corporation (MSFT)
- Apple Inc. (AAPL)
- Amazon.com Inc. (AMZN)
- Meta Platforms Inc. (META)

### 2. 📊 SPX Weekly Trend Analysis
- Analyzes SPX price movements over the past 7 trading days
- Identifies trends: Uptrend/Downtrend/Sideways
- Measures momentum: Strong/Moderate/Weak
- Provides technical context for trading decisions

### 3. 🏛️ Federal Reserve Policy Impact
- Latest FOMC decisions and meeting minutes
- Fed Chair (Jerome Powell) statements
- Interest rate outlook
- Inflation data and economic projections
- Market interpretation (Hawkish/Dovish/Neutral)

## Dynamic Features

### ✅ Automatically Handles:
- **Current Date & Time**: System fetches real-time date/time (October 30, 2025 2:04 AM)
- **Week Range**: Automatically calculates past 7 days for trend analysis
- **Current Month/Year**: Adapts prompts for any month/year
- **Trading Hours**: Shows 9:30 AM - 4:00 PM ET trading window
- **Weekend Detection**: Warns if run on Saturday/Sunday

### 🔄 Works Year-Round:
- January through December
- Automatically updates date references in searches
- No hardcoded dates - always uses current time
- Adapts to Fed meetings throughout the year

## How to Use

### Daily Trading Routine:
```bash
cd /Users/snehal/Documents/repos/agents/financial_researcher
crewai run
```

### Best Time to Run:
- **Morning**: 8:30-9:00 AM ET (before market opens)
- **Mid-Day**: 12:00-1:00 PM ET (lunch update)
- **End of Day**: 3:30-4:00 PM ET (closing analysis)

### What Gets Generated:

The system creates **9 output files** in the `output/` directory:

#### 📰 Individual Company News:
1. `nvidia_news.md` - Latest NVIDIA breaking news
2. `microsoft_news.md` - Latest Microsoft breaking news
3. `apple_news.md` - Latest Apple breaking news
4. `amazon.com_news.md` - Latest Amazon breaking news
5. `meta_news.md` - Latest Meta breaking news

#### 📊 Market Analysis:
6. `spx_weekly_analysis.md` - 📈 SPX price trends (past 7 days)
7. `fed_policy_analysis.md` - 🏛️ Federal Reserve policy impact
8. `comprehensive_analysis.md` - 📋 All data combined

#### 🎯 Trading Decision:
9. `spx_trading_signal.md` - ⭐ **FINAL BUY/SELL/HOLD RECOMMENDATION**

## Trading Signal Format

```
=== SPX TRADING SIGNAL ===
Generated: [Current Date & Time]
Current SPX: [Live Price]
Analysis Period: [Past Week Range]

RECOMMENDATION: BUY / SELL / HOLD
CONFIDENCE: High / Medium / Low
TARGET: [Price Level or Point Movement]
TIMEFRAME: [Today's session / Next 1-2 days]

INTEGRATED ANALYSIS:

1. TECH SECTOR IMPACT (50% of SPX)
   • Bullish Factors: [Key positive news]
   • Bearish Factors: [Key negative news]
   • Net Impact: [Positive/Negative/Neutral]

2. TECHNICAL TREND ANALYSIS
   • Weekly Trend: [Uptrend/Downtrend/Sideways]
   • Momentum: [Strong/Moderate/Weak]
   • Technical Bias: [Bullish/Bearish/Neutral]

3. FED POLICY IMPACT
   • Policy Stance: [Supportive/Restrictive/Neutral]
   • Recent Communications: [Positive/Negative]
   • Macro Bias: [Bullish/Bearish/Neutral]

KEY DRIVERS (Ranked):
1. [Most important factor]
2. [Second most important]
3. [Third most important]
4. [Fourth]
5. [Fifth]

RISK FACTORS:
- [Risk 1 with context]
- [Risk 2 with context]
- [Risk 3 with context]

CONCLUSION: [Clear trading thesis]

PRICE TARGETS:
- Upside Target: [Level]
- Downside Risk: [Level]
- Stop Loss: [Level if applicable]

Disclaimer: Not financial advice. Educational purposes only.
```

## Real-Time Data Sources

The system searches for:

### Tech News:
- "{Company} news today"
- "{Company} breaking news [current date]"
- "{Company} stock news latest"
- "{Company} earnings [current month] [current year]"

### SPX Data:
- "SPX price last week [current date]"
- "S&P 500 weekly chart [current month] [current year]"
- "SPX historical prices [week range]"

### Fed Policy:
- "Federal Reserve news today [current date]"
- "Fed interest rate decision [current month] [current year]"
- "Jerome Powell statement [current date]"
- "FOMC meeting [current month] [current year]"

## Example Timeline

### Monday Morning (9:00 AM ET):
- System fetches: News from Friday close through Monday pre-market
- SPX Analysis: Previous Monday - Friday data
- Fed Policy: Any weekend statements

### Wednesday Afternoon (2:00 PM ET):
- System fetches: Breaking news from last 24-48 hours
- SPX Analysis: Previous Wednesday - Current Wednesday
- Fed Policy: Any mid-week FOMC releases

### Friday Close (3:45 PM ET):
- System fetches: Week-ending news
- SPX Analysis: Full week Monday - Friday
- Fed Policy: Week's Fed communications

## Key Advantages

### 1. **Time-Aware**
- Always uses current date/time
- Searches are dynamically updated
- No outdated information

### 2. **Comprehensive**
- Combines 3 critical factors (tech + technical + macro)
- Weighs factors appropriately
- Provides integrated analysis

### 3. **Year-Round Applicable**
- Works January - December
- Adapts to Fed schedule changes
- Handles earnings seasons automatically

### 4. **Professional Grade**
- Clear BUY/SELL/HOLD signals
- Confidence levels
- Specific price targets
- Risk assessment

## Monitoring Your Trades

After receiving a signal:

1. **Check the comprehensive_analysis.md** for full context
2. **Review individual company news** for specific catalysts
3. **Verify SPX weekly trend** aligns with recommendation
4. **Assess Fed policy** impact on your timeframe
5. **Compare with live SPX** price at https://finance.yahoo.com/quote/%5ESPX/

## Important Notes

⚠️ **Disclaimer**: This system is for **educational purposes only**. Not financial advice.

📅 **Best Results**: Run during market hours (9:30 AM - 4:00 PM ET, Monday-Friday)

🔄 **Frequency**: Can be run multiple times per day as news develops

📊 **Live SPX**: Always check current price at Yahoo Finance before acting

🏛️ **Fed Calendar**: System tracks FOMC meetings automatically throughout the year

## Support

For issues or questions:
- Check output files for detailed analysis
- Review comprehensive_analysis.md for full context
- Verify .env file has OPENAI_API_KEY and SERPER_API_KEY

## Future Enhancements

Potential additions:
- Real-time SPX price API integration
- SMS/Email alerts for HIGH confidence signals
- Backtesting with historical data
- Options flow analysis
- Sector rotation signals

---

**Last Updated**: System is dynamic and updates automatically
**System Status**: ✅ Operational Year-Round
**Trading Hours**: 9:30 AM - 4:00 PM ET, Monday-Friday

