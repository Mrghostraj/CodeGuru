import requests
import gradio as gr

# ============================================================
# CodeGuru — AI Coding Assistant
# Gradio 6 + Ollama
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codeguru:latest"

LANGUAGES = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "PHP",
    "SQL",
]

# ============================================================
# Ollama
# ============================================================

def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        if response.status_code != 200:
            return (
                f"### ⚠️ Ollama Error\n\n"
                f"**HTTP {response.status_code}**\n\n"
                f"```text\n{response.text}\n```"
            )

        data = response.json()
        return data.get("response", "No response received from CodeGuru.")

    except requests.exceptions.ConnectionError:
        return (
            "### 🔴 Ollama is not reachable\n\n"
            "Make sure Ollama is running on `localhost:11434`."
        )

    except requests.exceptions.Timeout:
        return (
            "### ⏳ Request timed out\n\n"
            "CodeLlama took too long to generate a response."
        )

    except Exception as e:
        return f"### ❌ Unexpected error\n\n```text\n{str(e)}\n```"


# ============================================================
# Prompt builders
# ============================================================

def build_generate_prompt(language, request):
    return f"""
You are CodeGuru, an AI coding assistant.

Programming Language: {language}

Task:
{request}

Generate the solution strictly in {language}.

Requirements:
- Give complete runnable code.
- Keep the implementation clean and readable.
- Explain the approach briefly.
- Mention time and space complexity when relevant.
- Include important edge cases.
- Do not switch to another programming language.

Return the answer in this structure:

## Approach
Brief explanation.

## Code
```{language.lower()}
complete code here
```

## Complexity
Time and space complexity.

## Example
Show a small example if useful.
"""


def build_debug_prompt(language, code, request):
    extra = request.strip() if request.strip() else "No additional instructions."

    return f"""
You are CodeGuru, an AI coding reviewer and debugger.

Programming Language: {language}

User's Code:
```{language.lower()}
{code}
```

Additional User Request:
{extra}

Analyze the submitted code carefully.

Do NOT blindly rewrite the entire solution.

Return the answer using exactly this structure:

## Verdict
State whether the code is correct, partially correct, or incorrect.

## Issues
For every issue:
- Identify the exact problematic line or section.
- Explain what is wrong.
- Explain why it is wrong.

If there are no issues, clearly say so.

## Corrected Code
Provide a complete corrected version only when correction is needed.
If the original code is already correct, show an improved version only if there is a meaningful improvement.

## Explanation
Explain the important corrections.

## Test Cases
Provide useful test cases, including edge cases.

## Complexity
Give time and space complexity.

Programming language must remain {language}.
"""


# ============================================================
# Generate mode
# ============================================================

def generate_code(language, request):
    if not request.strip():
        return "### ✏️ Tell me what you want to build first."

    prompt = build_generate_prompt(language, request)
    return call_ollama(prompt)


# ============================================================
# Debug mode
# ============================================================

def debug_code(language, code, request):
    if not code.strip():
        return "### 🐛 Paste your code first so CodeGuru can analyze it."

    prompt = build_debug_prompt(language, code, request)
    return call_ollama(prompt)


# ============================================================
# CSS — Warm Orange / Charcoal Theme
# ============================================================

CSS = """
:root {
    --orange: #f97316;
    --orange-dark: #ea580c;
    --orange-soft: #fb923c;
    --bg: #0f0d0b;
    --panel: #171310;
    --panel-2: #1d1814;
    --editor: #211b17;
    --border: #332a24;
    --text: #f5f5f4;
    --muted: #a8a29e;
}

.gradio-container {
    max-width: 1500px !important;
    margin: 0 auto !important;
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

body {
    background: var(--bg) !important;
}

/* Header */
.cg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 18px 24px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}

.cg-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.cg-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #fb923c, #ea580c);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #171310;
    font-size: 21px;
    font-weight: 900;
    box-shadow: 0 8px 28px rgba(249, 115, 22, 0.20);
}

.cg-title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.cg-subtitle {
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.cg-status {
    color: #a8a29e;
    font-size: 12px;
    padding: 8px 12px;
    border: 1px solid var(--border);
    border-radius: 999px;
    background: #14110f;
}

/* Sidebar */
.cg-sidebar {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 18px !important;
    min-height: 650px;
}

.cg-sidebar-title {
    color: var(--muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin: 4px 0 14px 4px;
}

.cg-mode-note {
    color: #78716c;
    font-size: 12px;
    line-height: 1.5;
    margin: 16px 4px;
}

/* Main cards */
.cg-card {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 22px !important;
}

.cg-section-title {
    font-size: 19px;
    font-weight: 750;
    margin-bottom: 4px;
}

.cg-section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 20px;
}

/* Labels */
label span {
    color: #d6d3d1 !important;
    font-weight: 600 !important;
}

/* Inputs */
textarea,
input,
select {
    background: var(--editor) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

textarea:focus,
input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 1px rgba(249, 115, 22, 0.18) !important;
}

/* Code editor */
.cm-editor,
.cm-scroller,
.cm-gutters {
    background: #14110f !important;
}

.cm-editor {
    border-radius: 10px !important;
}

.cm-editor.cm-focused {
    outline: 1px solid rgba(249, 115, 22, 0.65) !important;
}

/* Buttons */
button {
    transition: all 0.15s ease !important;
}

.cg-primary button,
button.cg-primary {
    background: linear-gradient(135deg, #fb923c, #ea580c) !important;
    color: #171310 !important;
    border: none !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 24px rgba(249, 115, 22, 0.16) !important;
}

.cg-primary button:hover,
button.cg-primary:hover {
    background: linear-gradient(135deg, #fdba74, #f97316) !important;
    transform: translateY(-1px);
}

.cg-secondary button {
    background: #211b17 !important;
    color: #e7e5e4 !important;
    border: 1px solid var(--border) !important;
}

.cg-secondary button:hover {
    border-color: var(--orange) !important;
    color: #fb923c !important;
}

/* Radio / mode selector */
.cg-radio label {
    background: #1b1612 !important;
    border: 1px solid var(--border) !important;
    color: #d6d3d1 !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    margin-bottom: 8px !important;
}

.cg-radio label:has(input:checked) {
    background: rgba(249, 115, 22, 0.12) !important;
    border-color: var(--orange) !important;
    color: #fb923c !important;
}

/* Markdown output */
.cg-output {
    background: #14110f !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    min-height: 350px;
}

.cg-output h2 {
    color: #fb923c !important;
    font-size: 16px !important;
    margin-top: 18px !important;
}

.cg-output code {
    background: #211b17 !important;
}

.cg-output pre {
    background: #0c0a09 !important;
    border: 1px solid #30261f !important;
    border-radius: 10px !important;
}

/* Footer */
.cg-footer {
    text-align: center;
    color: #57534e;
    font-size: 11px;
    padding: 20px 0 8px 0;
}

/* Hide unnecessary Gradio footer */
footer {
    display: none !important;
}

/* Responsive */
@media (max-width: 900px) {
    .cg-sidebar {
        min-height: auto;
    }
}
"""


# ============================================================
# UI
# ============================================================

with gr.Blocks(title="CodeGuru — AI Coding Assistant") as app:

    gr.HTML(
        """
        <div class="cg-header">
            <div class="cg-brand">
                <div class="cg-logo">⚡</div>
                <div>
                    <div class="cg-title">CodeGuru</div>
                    <div class="cg-subtitle">
                        AI-powered coding assistant
                    </div>
                </div>
            </div>

            <div class="cg-status">
                ● Local AI · Ollama
            </div>
        </div>
        """
    )

    with gr.Row(equal_height=False):

        # ----------------------------------------------------
        # Sidebar
        # ----------------------------------------------------
        with gr.Column(scale=1, elem_classes="cg-sidebar"):

            gr.HTML(
                '<div class="cg-sidebar-title">Code Mode</div>'
            )

            mode = gr.Radio(
                choices=["💻 Generate", "🐛 Debug / Review", "🧠 Practice"],
                value="💻 Generate",
                show_label=False,
                elem_classes="cg-radio",
            )

            gr.HTML(
                """
                <div class="cg-mode-note">
                    <b>Generate</b><br>
                    Turn your ideas into working code.<br><br>

                    <b>Debug / Review</b><br>
                    Find mistakes and understand how to fix them.<br><br>

                    <b>Practice</b><br>
                    Coming next — solve coding problems with CodeGuru.
                </div>
                """
            )

            gr.Markdown(
                """
                **CodeGuru V1**

                `CodeLlama` · `Ollama` · `Gradio`
                """,
                elem_classes="cg-mode-note",
            )

        # ----------------------------------------------------
        # Main content
        # ----------------------------------------------------
        with gr.Column(scale=4):

            # =================================================
            # Generate
            # =================================================
            with gr.Column(visible=True, elem_classes="cg-card") as generate_panel:

                gr.HTML(
                    """
                    <div class="cg-section-title">Generate Code</div>
                    <div class="cg-section-subtitle">
                        Describe what you want to build and CodeGuru will write it for you.
                    </div>
                    """
                )

                generate_language = gr.Dropdown(
                    choices=LANGUAGES,
                    value="Python",
                    label="Programming Language",
                    info="CodeGuru will generate code in this language.",
                )

                generate_request = gr.Textbox(
                    label="What do you want to build?",
                    placeholder=(
                        "Example: Write a function that finds duplicate "
                        "elements in an array..."
                    ),
                    lines=5,
                )

                with gr.Row():
                    generate_btn = gr.Button(
                        "⚡ Generate Code",
                        variant="primary",
                        elem_classes="cg-primary",
                        scale=3,
                    )

                    clear_generate = gr.Button(
                        "Clear",
                        elem_classes="cg-secondary",
                        scale=1,
                    )

                generate_output = gr.Markdown(
                    value=(
                        "### 👋 Welcome to CodeGuru\n\n"
                        "Choose a programming language and describe what "
                        "you want to build."
                    ),
                    elem_classes="cg-output",
                )

            # =================================================
            # Debug
            # =================================================
            with gr.Column(
                visible=False,
                elem_classes="cg-card"
            ) as debug_panel:

                gr.HTML(
                    """
                    <div class="cg-section-title">Debug & Review</div>
                    <div class="cg-section-subtitle">
                        Paste your code. CodeGuru will identify mistakes,
                        explain them, and provide a corrected version.
                    </div>
                    """
                )

                debug_language = gr.Dropdown(
                    choices=LANGUAGES,
                    value="Python",
                    label="Programming Language",
                )

                debug_code_input = gr.Code(
                    language="python",
                    label="Your Code",
                    lines=18,
                )

                debug_request = gr.Textbox(
                    label="Additional instructions (optional)",
                    placeholder=(
                        "Example: Why is this giving a wrong answer "
                        "for an empty array?"
                    ),
                    lines=3,
                )

                with gr.Row():
                    debug_btn = gr.Button(
                        "🐛 Analyze Code",
                        variant="primary",
                        elem_classes="cg-primary",
                        scale=3,
                    )

                    clear_debug = gr.Button(
                        "Clear",
                        elem_classes="cg-secondary",
                        scale=1,
                    )

                debug_output = gr.Markdown(
                    value=(
                        "### 🐛 Ready to review your code\n\n"
                        "Paste your code above and click **Analyze Code**."
                    ),
                    elem_classes="cg-output",
                )

            # =================================================
            # Practice placeholder
            # =================================================
            with gr.Column(
                visible=False,
                elem_classes="cg-card"
            ) as practice_panel:

                gr.HTML(
                    """
                    <div class="cg-section-title">Practice Mode</div>
                    <div class="cg-section-subtitle">
                        Practice mode is the next CodeGuru module.
                    </div>
                    """
                )

                gr.Markdown(
                    """
                    ### 🧠 Coming Next

                    CodeGuru Practice will let you:

                    - Choose a programming language
                    - Choose a difficulty
                    - Choose a topic
                    - Generate coding problems
                    - Write your solution
                    - Submit your code
                    - Receive feedback
                    - Get complexity analysis
                    - Track your progress
                    """,
                    elem_classes="cg-output",
                )

    gr.HTML(
        """
        <div class="cg-footer">
            CodeGuru · Built locally with Ollama + CodeLlama
        </div>
        """
    )

    # ========================================================
    # Mode switching
    # ========================================================

    def switch_mode(selected):
        return (
            gr.update(visible=selected == "💻 Generate"),
            gr.update(visible=selected == "🐛 Debug / Review"),
            gr.update(visible=selected == "🧠 Practice"),
        )

    mode.change(
        fn=switch_mode,
        inputs=mode,
        outputs=[generate_panel, debug_panel, practice_panel],
    )

    # ========================================================
    # Generate events
    # ========================================================

    generate_btn.click(
        fn=generate_code,
        inputs=[generate_language, generate_request],
        outputs=generate_output,
    )

    clear_generate.click(
        fn=lambda: ("", "### 👋 Ready for your next idea."),
        outputs=[generate_request, generate_output],
    )

    # ========================================================
    # Debug events
    # ========================================================

    debug_btn.click(
        fn=debug_code,
        inputs=[debug_language, debug_code_input, debug_request],
        outputs=debug_output,
    )

    clear_debug.click(
        fn=lambda: ("", "", "### 🐛 Ready to review your code."),
        outputs=[debug_code_input, debug_request, debug_output],
    )


# ============================================================
# Launch
# ============================================================

if __name__ == "__main__":
    app.launch(
        theme=gr.themes.Base(
            primary_hue="orange",
            neutral_hue="stone",
        ),
        css=CSS,
    )
