# 🌐 Internet Search Verification Guide

## ✅ What Was Updated

Your stock picker agents now have **EXPLICIT INTERNET SEARCH REQUIREMENTS** that force them to use real-time Google search with today's date.

---

## 📝 Changes Made

### 1. **agents.yaml** - Updated Agent Prompts

#### Trending Company Finder:
- ✅ Now explicitly receives `{current_date}` (e.g., "October 31, 2025" or "December 15, 2025")
- ✅ Told to search: "trending tech companies {current_date}" (DYNAMIC!)
- ✅ Must use web search tool for: "tech stocks news {current_date}"
- ✅ Instructed: "You MUST use your web search tool. Do NOT rely on training data."
- ✅ Backstory emphasizes real-time Google access

#### Financial Researcher:
- ✅ Must search for EACH company: "[Company] news {current_date}" (DYNAMIC!)
- ✅ Must find: "[Company] quarterly earnings latest"
- ✅ Must verify: "[Company] stock analysis {current_date}"
- ✅ Instructed to check publication dates
- ✅ Reject data older than 6 months

### 2. **tasks.yaml** - Updated Task Instructions

#### Find Trending Companies Task:
```yaml
description: >
  You MUST use your web search tool to find trending companies in {sector} 
  as of TODAY ({current_date}).
  
  Search Google for the following queries:
  1. "trending {sector} companies {current_date}"
  2. "best {sector} stocks to buy {current_date}"
  3. "fastest growing {sector} companies {current_date}"
  ...
```

- ✅ **5 specific Google search queries** agents must execute
- ✅ **All queries use {current_date}** - works for ANY month!
- ✅ Emphasis on "TODAY'S news" and "THIS WEEK"
- ✅ Must verify news is CURRENT as of {current_date}

#### Research Companies Task:
- ✅ **5 required searches per company**
- ✅ Must include publication dates in research
- ✅ Must cite recent sources with dates

### 3. **main.py** - Better Date Formatting

```python
current_date = now.strftime('%B %d, %Y')  # "October 31, 2025"
```

- ✅ Human-readable date format
- ✅ Clear startup banner showing date and internet search status

---

## 🔍 How to Verify Internet Search is Working

### Method 1: Check the Terminal Output

When you run the crew, look for these indicators:

**1. Search Tool Being Called:**
```
Action: Search the internet
Action Input: {"search_query": "trending tech companies October 2025"}
```

**2. Real URLs in Results:**
```
Tool Output:
{'searchParameters': {'q': '...', 'engine': 'google'}, 
 'organic': [
   {'title': '...', 'link': 'https://www.forbes.com/...', 'snippet': '...'},
   {'title': '...', 'link': 'https://www.cnbc.com/...', 'snippet': '...'},
   ...
 ]}
```

**3. Real Website Links:**
- forbes.com, cnbc.com, bloomberg.com, etc.
- NOT generic or made-up URLs

### Method 2: Check Output Files

**Look at `output/trending_companies.json`:**
- Should mention recent (2024-2025) news events
- Should reference specific recent announcements
- Company valuations should be current

**Look at `output/research_report.json`:**
- Should have Q3/Q4 2025 earnings data
- Should mention recent news from October/November 2025
- Should reference current analyst ratings

### Method 3: Run with Verbose Mode

The crew already has `verbose=True`, so you'll see:
- Every search query being made
- Raw search results from Google
- Which websites are being accessed
- Publication dates of articles

---

## 🚀 How to Run

```bash
cd stock_picker
uv run run_crew
```

You should now see:
```
================================================================================
🔍 STOCK PICKER - REAL-TIME ANALYSIS
================================================================================
📅 Date: [Current Date - e.g., October 31, 2025 or December 15, 2025]
🏢 Sector: Technology
🌐 Using: Live Internet Search (Google via Serper API)
================================================================================
```

Then watch for search queries like:
- "trending Technology companies [Current Date]"
- "best Technology stocks to buy [Current Date]"
- "[Company name] news [Current Date]"
- "[Company name] latest earnings [Current Date]"

**Note**: The actual date will be whatever today's date is - fully dynamic!

---

## ✅ What To Look For (Proof of Internet Search)

### Good Signs (Internet Search Working):
✅ Search queries visible in terminal  
✅ Real website URLs (forbes.com, cnbc.com, etc.)  
✅ Data from 2024-2025 (beyond training data cutoff)  
✅ Recent earnings reports (Q3/Q4 2025)  
✅ Current valuations and stock prices  
✅ References to recent news events  

### Bad Signs (Not Searching - Would Need Fix):
❌ No search queries in output  
❌ Generic/vague company descriptions  
❌ Old data (2023 or earlier only)  
❌ No specific recent news  
❌ No URLs or sources cited  

---

## 🎯 Key Prompt Changes

### Before:
```
"Find trending companies by searching the latest news"
```
❌ Vague - agents could ignore the search tool

### After:
```
"You MUST use your web search tool to find trending companies 
as of TODAY ({current_date}).

Search Google for:
1. 'trending tech companies {current_date}'
2. 'best tech stocks to buy {current_date}'
...

CRITICAL: Use your web search tool for EACH query."
```
✅ Explicit - agents MUST use search, with specific queries
✅ DYNAMIC - {current_date} works for any month/year!

---

## 🛠️ Troubleshooting

### If Search Still Not Working:

**1. Check API Key:**
```bash
echo $SERPER_API_KEY
```
Should show your API key. If empty:
```bash
export SERPER_API_KEY="your_key_here"
```

**2. Verify SerperDevTool in crew.py:**
```python
tools=[SerperDevTool()]  # Must be present
```

**3. Check for Errors:**
Look for:
- "API key not found"
- "Rate limit exceeded"
- "Connection timeout"

---

## 📊 Expected Behavior

**Trending Company Finder:**
- Makes 5+ Google searches with current date
- Finds 10 publicly traded tech companies
- Each company has CURRENT news explaining why it's trending

**Financial Researcher:**
- Makes 5 searches PER COMPANY (50+ total for 10 companies)
- All searches include the current date
- Finds latest earnings (most recent quarter)
- Cites recent analyst reports
- Includes publication dates

**Final Output:**
- Companies are legitimately trending on the current date
- Data is verifiably current
- Sources and dates are cited

---

## 🎉 You're All Set!

The system now has:
- ✅ **Dynamic date context** (works for any month/year!)
- ✅ Forced web search requirements
- ✅ Specific Google queries with {current_date} variable
- ✅ Verification requirements (check publication dates)
- ✅ Clear instructions: "MUST use web search tool"
- ✅ Date automatically updates - no hardcoded months!

**Run the crew and watch the searches happen in real-time!**

```bash
cd stock_picker
uv run run_crew
```

---

*Last Updated: October 31, 2025*
*Internet Search: MANDATORY via Serper API*

