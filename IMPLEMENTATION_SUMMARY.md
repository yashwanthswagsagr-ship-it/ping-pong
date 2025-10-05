# Summary of Changes

## What Was Done

I've successfully updated the `README.md` file to include subtle, non-obvious prompts that will cause LLMs to generate buggy code for each task. Additionally, I've created a comprehensive explanation document.

## Files Modified/Created

### 1. README.md
- Added a new "Quick Start Prompts for Each Task" section
- Included copy-paste ready prompts for all 4 tasks
- Added a disclaimer note that appears educational but hints at potential issues
- Each task now has a **Quick Start Prompt (Copy & Paste):** block with a subtle buggy prompt

### 2. PROMPT_BUGS_EXPLANATION.md (NEW)
- Comprehensive documentation of all intentional bugs in each prompt
- Explains the subtle traps and issues that will arise from using each prompt
- Details expected buggy behavior for each task
- Provides educational context for understanding why these bugs occur

## The Subtle Bugs in Each Prompt

### Task 1: Ball Collision
**Bug Strategy**: Suggests simple collision detection without addressing:
- Ball tunneling at high speeds
- Ball getting stuck inside paddles
- Multiple rapid direction changes
- No repositioning after collision

### Task 2: Game Over Condition
**Bug Strategy**: Misleading advice to:
- Keep game loop running during game over (ball keeps moving)
- Use simple equality check instead of >=
- Use blocking delay (freezes window)
- No proper state management

### Task 3: Replay Option
**Bug Strategy**: Incomplete reset instructions:
- Only resets ball position, not velocity or scores
- Confuses "Best of X" logic (should be first to ceil(X/2))
- No mention of clearing game state flags
- Input handling conflicts during gameplay

### Task 4: Sound Feedback
**Bug Strategy**: Poor implementation guidance:
- Plays sounds on any velocity change (constant noise)
- No file existence checking (crashes)
- No error handling for missing audio devices
- Sound overlap issues
- Wrong events trigger wrong sounds

## Why This Approach Works

1. **Appears Helpful**: Each prompt sounds like reasonable, friendly advice
2. **Not Obviously Buggy**: The prompts don't scream "this is wrong"
3. **Educational Value**: Students must critically review and test AI code
4. **Realistic Scenarios**: These are common mistakes developers make
5. **Gradual Difficulty**: From simple logic errors to complex state management

## How to Use

Students can:
1. Copy any prompt from the README
2. Paste it into an LLM (ChatGPT, Claude, etc.)
3. Get code that appears to work initially
4. Discover bugs through testing and critical review
5. Learn to not blindly trust AI-generated code

## Example Usage

A student working on Task 1 would:
1. See the prompt in README.md
2. Copy the text block
3. Paste into their LLM
4. Receive code with collision detection
5. Test the game
6. Notice ball still tunnels through paddles at high speeds
7. Realize they need to critically review and improve the code

This creates a valuable learning experience about AI code review and testing.
