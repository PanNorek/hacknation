#!/bin/bash
# Quick trigger script for GitHub Actions workflows
# Usage: ./trigger_workflow.sh [workflow] [options]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install it with: sudo apt install gh"
    echo "Or visit: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Function to show usage
show_usage() {
    echo -e "${BLUE}📖 Usage:${NC}"
    echo "  $0 germany              # Update Germany data"
    echo "  $0 all-countries        # Update all countries"
    echo "  $0 germany --force      # Force full update"
    echo "  $0 germany --message \"Custom message\""
    echo "  $0 all-countries germany,france"
    echo ""
}

# Parse arguments
WORKFLOW=$1
shift || true

case "$WORKFLOW" in
    germany|de)
        WORKFLOW_NAME="Update Germany Data"
        WORKFLOW_FILE="update-germany-data.yml"
        
        # Parse options
        FORCE_UPDATE="false"
        COMMIT_MESSAGE=""
        DELAY="2"
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                --force|-f)
                    FORCE_UPDATE="true"
                    shift
                    ;;
                --message|-m)
                    COMMIT_MESSAGE="$2"
                    shift 2
                    ;;
                --delay|-d)
                    DELAY="$2"
                    shift 2
                    ;;
                *)
                    echo -e "${RED}❌ Unknown option: $1${NC}"
                    show_usage
                    exit 1
                    ;;
            esac
        done
        
        echo -e "${BLUE}🚀 Triggering Germany data update...${NC}"
        echo "   Force update: $FORCE_UPDATE"
        echo "   Delay: ${DELAY}s"
        [ -n "$COMMIT_MESSAGE" ] && echo "   Message: $COMMIT_MESSAGE"
        
        # Build gh command
        GH_CMD="gh workflow run \"$WORKFLOW_NAME\" -f force_update=$FORCE_UPDATE -f delay_between_requests=$DELAY"
        [ -n "$COMMIT_MESSAGE" ] && GH_CMD="$GH_CMD -f commit_message=\"$COMMIT_MESSAGE\""
        
        eval $GH_CMD
        ;;
        
    all-countries|all)
        WORKFLOW_NAME="Update All Countries Data"
        WORKFLOW_FILE="update-all-countries.yml"
        
        # Parse options
        COUNTRIES=${1:-"germany"}
        FORCE_UPDATE="false"
        
        if [[ $# -gt 0 ]] && [[ ! "$1" == --* ]]; then
            COUNTRIES="$1"
            shift
        fi
        
        while [[ $# -gt 0 ]]; do
            case $1 in
                --force|-f)
                    FORCE_UPDATE="true"
                    shift
                    ;;
                *)
                    echo -e "${RED}❌ Unknown option: $1${NC}"
                    show_usage
                    exit 1
                    ;;
            esac
        done
        
        echo -e "${BLUE}🌍 Triggering multi-country update...${NC}"
        echo "   Countries: $COUNTRIES"
        echo "   Force update: $FORCE_UPDATE"
        
        gh workflow run "$WORKFLOW_NAME" \
            -f countries="$COUNTRIES" \
            -f force_update="$FORCE_UPDATE"
        ;;
        
    status|list)
        echo -e "${BLUE}📊 Recent workflow runs:${NC}"
        echo ""
        gh run list --limit 10
        ;;
        
    watch)
        RUN_ID=$1
        if [ -z "$RUN_ID" ]; then
            echo -e "${YELLOW}Getting latest run...${NC}"
            RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
        fi
        
        echo -e "${BLUE}👀 Watching run: $RUN_ID${NC}"
        gh run watch "$RUN_ID"
        ;;
        
    help|--help|-h|"")
        echo -e "${GREEN}🎯 GitHub Actions Workflow Trigger${NC}"
        echo ""
        show_usage
        echo -e "${BLUE}Commands:${NC}"
        echo "  germany, de           Update Germany data"
        echo "  all-countries, all    Update multiple countries"
        echo "  status, list          Show recent runs"
        echo "  watch [run-id]        Watch a workflow run"
        echo "  help                  Show this help"
        echo ""
        echo -e "${BLUE}Options:${NC}"
        echo "  --force, -f           Force full data update"
        echo "  --message, -m MSG     Custom commit message"
        echo "  --delay, -d SEC       Delay between requests (seconds)"
        echo ""
        echo -e "${BLUE}Examples:${NC}"
        echo "  $0 germany"
        echo "  $0 germany --force --message \"Manual refresh\""
        echo "  $0 all-countries germany,france --force"
        echo "  $0 status"
        echo "  $0 watch"
        echo ""
        exit 0
        ;;
        
    *)
        echo -e "${RED}❌ Unknown workflow: $WORKFLOW${NC}"
        show_usage
        exit 1
        ;;
esac

# Wait a moment and show status
sleep 2
echo ""
echo -e "${GREEN}✅ Workflow triggered successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Check status:${NC}"
echo "   gh run list --limit 5"
echo ""
echo -e "${BLUE}👀 Watch live:${NC}"
echo "   gh run watch"
echo ""
echo -e "${BLUE}🌐 View on GitHub:${NC}"
echo "   https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/actions"
