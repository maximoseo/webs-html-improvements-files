# SKILL: SwiftUI Agent Skill (SwiftUI Pro)
**Source:** https://github.com/twostraws/SwiftUI-Agent-Skill
**Domain:** design
**Trigger:** When writing SwiftUI code, reviewing SwiftUI for iOS/macOS, or fixing LLM-generated SwiftUI mistakes

## Summary
An agent skill that helps AI coding assistants write smarter, simpler, and more modern SwiftUI. Targets iOS 26+ and Swift 6.2+. Covers navigation, layout, animations, state management, VoiceOver accessibility, deprecated APIs, and common LLM mistakes — built on thousands of hours of real-world SwiftUI experience.

## Key Patterns
- **Navigation**: NavigationStack/NavigationSplitView over deprecated NavigationView; use `navigationDestination(for:)` for type-safe navigation
- **Layout**: ViewThatFits, Grid, LazyVGrid over manual frame calculations; avoid `.frame(width:height:)` for flexible layouts
- **Animations**: `.animation(_:value:)` over deprecated `.animation(_:)`; use `withAnimation {}` for explicit state changes
- **State management**: `@Observable` (iOS 17+) over `ObservableObject`/`@Published`; `@Environment` for dependency injection
- **VoiceOver**: Every interactive element needs `.accessibilityLabel`; buttons invisible to VoiceOver without it
- **Deprecated API**: NavigationView, `List { ForEach }` with indices, `UIApplication.shared.windows`, `.onChange(of:)` single-param form
- **Performance**: `LazyVStack`/`LazyHStack` for long lists; avoid `@State` in views that rebuild frequently
- **iOS 26 specifics**: Liquid Glass materials, new toolbar behaviors, updated sheet detents

## Usage
Install: `npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro`

Via Claude Code: `/swiftui-pro`  
Via Codex: `$swiftui-pro`

Partial reviews: `/swiftui-pro Check for deprecated API` or `/swiftui-pro Focus on accessibility`

## Code/Template
```swift
// CORRECT: Modern navigation (iOS 16+)
NavigationStack {
    List(items) { item in
        NavigationLink(value: item) { ItemRow(item: item) }
    }
    .navigationDestination(for: Item.self) { item in ItemDetail(item: item) }
}

// WRONG: Deprecated
NavigationView { /* ... */ }

// CORRECT: Observable (iOS 17+)
@Observable class ViewModel { var count = 0 }

// WRONG: Old pattern
class ViewModel: ObservableObject { @Published var count = 0 }

// CORRECT: Accessible button
Button("Delete") { delete() }
    .accessibilityLabel("Delete item")
    .accessibilityHint("Removes this item from your list")

// CORRECT: Lazy list for performance
LazyVStack {
    ForEach(items) { item in ItemRow(item: item) }
}
```
