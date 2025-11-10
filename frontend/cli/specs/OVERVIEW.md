# Beaver Go CLI - Project Overview

## Vision

Beaver is a **MonkeyType-inspired typing practice application** specifically designed for developers who want to improve their typing speed while simultaneously practicing and memorizing well-known algorithms and data structures. By combining typing practice with algorithm learning, Beaver provides dual value: improved muscle memory for coding patterns and enhanced typing proficiency.

## What is Beaver?

Beaver transforms the mundane task of typing practice into an engaging and educational experience. Instead of typing random text, users type real, production-quality algorithm implementations across various programming languages. Each practice session reinforces:

- **Typing Speed & Accuracy**: Real-time feedback on mistakes, typing speed (CPM), and accuracy
- **Algorithm Familiarity**: Exposure to classic algorithms (sorting, searching, graph traversal, dynamic programming)
- **Code Pattern Memory**: Muscle memory for common coding patterns and syntax
- **Language Proficiency**: Practice in multiple programming languages

## The Go CLI Project

This project aims to rewrite the existing Python-based TUI application in **Go using the Bubble Tea framework**. The Go version will maintain the core experience while introducing improvements in:

### Key Improvements Over Python Version

1. **Enhanced Editing Experience**
   - Allow backspace/editing during typing practice
   - More forgiving for learners while still tracking corrections
   - Natural typing flow similar to actual coding

2. **Redesigned Keyboard Shortcuts**
   - Modern, intuitive keybindings optimized for terminal use
   - Consistent with popular CLI tools
   - Improved discoverability

3. **Simplified Statistics Display**
   - Focus on actionable metrics: time, CPM, accuracy, error count
   - Clean, readable output without complex charts
   - Instant feedback after completion

4. **Performance Benefits**
   - Faster startup and response times
   - Efficient memory usage with Go's concurrency primitives
   - Native binary distribution (no Python runtime required)

5. **Maintainability**
   - Strong typing with Go's type system
   - Simpler deployment (single binary)
   - Better error handling patterns

## Target Audience

### Primary Users
- **Software Engineers**: Want to improve typing speed while coding
- **Students**: Learning algorithms and data structures
- **Technical Interviewers**: Practicing algorithm implementations
- **Career Switchers**: Building coding muscle memory

### Use Cases

1. **Daily Typing Practice**
   - 10-15 minute warmup before coding sessions
   - Build typing speed and accuracy over time
   - Track improvement in both speed and algorithm knowledge

2. **Algorithm Interview Prep**
   - Type out classic algorithms from memory
   - Build confidence for live coding interviews
   - Practice under time pressure

3. **Learning New Languages**
   - Practice syntax in different programming languages
   - Build familiarity with language-specific patterns
   - Compare algorithm implementations across languages

4. **Coding Warmup**
   - Get "in the zone" before starting work
   - Refresh algorithm knowledge
   - Improve focus and concentration

## Core Philosophy

### 1. Simplicity First
The CLI should be immediately usable without documentation. Core functionality should be discoverable through intuitive shortcuts and minimal UI chrome.

### 2. Focused Experience
No distractions, no unnecessary features. Just code, typing, and statistics. The terminal provides a distraction-free environment perfect for deliberate practice.

### 3. Real Code, Real Learning
All practice content consists of actual, working algorithm implementations. No pseudo-code, no simplified examples. Users type production-quality code.

### 4. Immediate Feedback
Real-time visual feedback on typing accuracy. Instant statistics after completion. No waiting, no loading screens.

### 5. Offline-First with Online Enhancement
The CLI should work seamlessly with occasional network issues. Background prefetching ensures smooth experience even with intermittent connectivity.

## Differentiators from Competitors

### vs. MonkeyType
- **Code-specific content**: Algorithms instead of prose
- **Syntax awareness**: Proper code highlighting and structure
- **Educational value**: Learn algorithms while practicing typing

### vs. Typing.io (defunct)
- **Open source**: Community-driven, free forever
- **Modern tech stack**: Bubble Tea framework, active development
- **Broader language support**: Easy to add new languages via dataset

### vs. Generic Typing Tutors
- **Domain-specific**: Built for programmers
- **Real-world practice**: Actual code patterns from real projects
- **Terminal-native**: Fits developer workflow

## Success Metrics

A successful Go CLI implementation will achieve:

1. **Usability**: New users can start typing within 5 seconds of launch
2. **Performance**: Sub-second response times for all interactions
3. **Reliability**: Graceful handling of network issues and edge cases
4. **Maintainability**: Clean codebase that's easy to extend with new features
5. **User Satisfaction**: Positive feedback on typing experience and learning value

## Project Scope

### In Scope
- Core typing practice functionality
- Syntax highlighting for code
- Real-time statistics tracking
- Background prefetching of algorithms
- Filter by language and tags
- Settings management
- Help system
- Theme support (dark/light)
- Error handling and edge cases

### Out of Scope (Future Enhancements)
- User accounts and authentication
- Cloud statistics storage
- Leaderboards and social features
- Custom algorithm uploads
- Mobile versions
- Web interface
- IDE plugins

## Technology Foundation

The Go CLI will be built on:

- **Go 1.21+**: Modern Go with generics support
- **Bubble Tea**: Production-ready TUI framework from Charm
- **Chroma**: Syntax highlighting for 200+ languages
- **Existing Beaver API**: Leverages the Go backend already in place

## Next Steps

This overview document serves as the foundation for:

1. **Features Specification**: Detailed breakdown of all features
2. **User Flows**: Step-by-step interaction patterns
3. **Keyboard Shortcuts**: Complete keybinding specification
4. **Technical Stack**: Library choices and justifications
5. **Architecture Design**: Technical implementation approach
6. **Implementation Roadmap**: Development phases and tickets

---

**Document Status**: Draft v1.0
**Last Updated**: 2025-11-10
**Owner**: Beaver Development Team
