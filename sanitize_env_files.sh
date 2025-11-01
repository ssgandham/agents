#!/bin/bash
# Script to sanitize all .env files by replacing actual keys with placeholders

echo "Sanitizing .env files..."

# 6_mcp/.env
cat > "./6_mcp/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
ANTHROPIC_API_KEY=enter_your_anthropic_api_key_here
EOF
echo "✓ Updated 6_mcp/.env"

# crewai projects/engineering_team/.env
cat > "./crewai projects/engineering_team/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
SERPER_API_KEY=enter_your_serper_api_key_here
EOF
echo "✓ Updated crewai projects/engineering_team/.env"

# crewai projects/financial_researcher/.env
cat > "./crewai projects/financial_researcher/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
SERPER_API_KEY=enter_your_serper_api_key_here
EOF
echo "✓ Updated crewai projects/financial_researcher/.env"

# crewai projects/debate/.env
cat > "./crewai projects/debate/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
SERPER_API_KEY=enter_your_serper_api_key_here
EOF
echo "✓ Updated crewai projects/debate/.env"

# crewai projects/coder/.env
cat > "./crewai projects/coder/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
EOF
echo "✓ Updated crewai projects/coder/.env"

# 3_crew/debate/.env
cat > "./3_crew/debate/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
SERPER_API_KEY=enter_your_serper_api_key_here
EOF
echo "✓ Updated 3_crew/debate/.env"

# 2_openai/.env
cat > "./2_openai/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
EOF
echo "✓ Updated 2_openai/.env"

# stock_picker/.env
cat > "./stock_picker/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
SERPER_API_KEY=enter_your_serper_api_key_here
PUSHOVER_USER_KEY=enter_your_pushover_user_key_here
PUSHOVER_APP_TOKEN=enter_your_pushover_app_token_here
EOF
echo "✓ Updated stock_picker/.env"

# 1_foundations/.env
cat > "./1_foundations/.env" << 'EOF'
OPENAI_API_KEY=enter_your_openai_api_key_here
ANTHROPIC_API_KEY=enter_your_anthropic_api_key_here
EOF
echo "✓ Updated 1_foundations/.env"

echo ""
echo "✅ All .env files have been sanitized!"
echo ""
echo "⚠️  IMPORTANT: These files now contain placeholders."
echo "Replace 'enter_your_*_key_here' with your actual API keys before running the projects."

