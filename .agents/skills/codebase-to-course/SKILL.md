# SKILL: Codebase to Course
**Source:** https://github.com/zarazhangrui/codebase-to-course
**Domain:** design
**Trigger:** When transforming a codebase, documentation, or technical content into an interactive HTML learning experience/course

## Summary
Converts any codebase or technical documentation into a polished, self-contained interactive HTML course with chapters, exercises, quizzes, and progress tracking — no backend required. Generates a single distributable HTML file.

## Key Patterns
- **Single-file output**: Self-contained HTML — no server, no dependencies to install
- **Auto-chapter generation**: Analyzes codebase structure → creates logical learning path
- **Interactive elements**: Code exercises with syntax highlighting, quizzes, progress tracking
- **AI-powered**: Uses LLMs to write explanations, exercises, and quiz questions from source code
- **Clean course UI**: Sidebar navigation, chapter progress, dark/light mode

## Usage
Provide a codebase or documentation folder → agent analyzes structure → generates course HTML.

Best for: open-source libraries, internal tools, onboarding materials, technical tutorials.

## Code/Template
```html
<!-- Generated course structure (single HTML file) -->
<!DOCTYPE html>
<html>
<head>
  <title>Learn [Project Name]</title>
  <!-- All CSS embedded inline -->
</head>
<body>
  <nav class="sidebar">
    <div class="chapter" data-chapter="1">1. Introduction</div>
    <div class="chapter" data-chapter="2">2. Core Concepts</div>
  </nav>
  <main class="content">
    <section class="chapter-content" id="ch1">
      <h2>Introduction</h2>
      <pre><code class="language-js">// Example from codebase</code></pre>
      <div class="quiz">
        <p>What does this function do?</p>
        <button onclick="check(this, true)">A. Correct answer</button>
        <button onclick="check(this, false)">B. Wrong answer</button>
      </div>
    </section>
  </main>
  <!-- All JS embedded inline -->
</body>
</html>
```
