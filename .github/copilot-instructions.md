# GitHub Copilot Instructions for Lórien's Guide

## Project Overview

Lórien's Guide is an accessibility tool designed to help vision-impaired individuals navigate public spaces. This project was created during Project Hafnia Hackathon with the goal of improving accessibility and independence for people with visual impairments.

## Core Principles

### Accessibility First
- **Always prioritize accessibility**: Every feature and UI element must be designed with accessibility in mind
- **WCAG Compliance**: Follow Web Content Accessibility Guidelines (WCAG) 2.1 Level AA or higher
- **Screen Reader Support**: Ensure all content is screen reader friendly with proper ARIA labels and semantic HTML
- **Keyboard Navigation**: All functionality must be accessible via keyboard
- **High Contrast**: Support high contrast modes and sufficient color contrast ratios (minimum 4.5:1 for text)

### Code Quality Standards
- Write clean, maintainable, and well-documented code
- Use descriptive variable and function names
- Add comments for complex logic or accessibility-specific implementations
- Follow the principle of least surprise - code should be intuitive

### Testing Requirements
- Write tests for all new features
- Include accessibility tests (e.g., aria attributes, keyboard navigation)
- Test with assistive technologies when possible
- Consider edge cases for users with different abilities

## Technology Guidelines

### General Coding Practices
- Use modern, accessible web technologies
- Optimize for performance (important for assistive technology)
- Ensure cross-browser compatibility
- Support mobile and desktop devices

### Accessibility Specific Code
- Use semantic HTML elements (`<nav>`, `<main>`, `<article>`, etc.)
- Include proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- Provide alternative text for all images and meaningful graphics
- Use `role`, `aria-label`, `aria-describedby` attributes appropriately
- Ensure form fields have associated labels
- Provide skip navigation links
- Use `<button>` for actions, `<a>` for navigation
- Include focus indicators that meet contrast requirements

### User Experience
- Design for voice control and gesture navigation
- Provide clear feedback for all user actions
- Use simple, clear language (avoid jargon)
- Implement generous tap/click targets (minimum 44x44 pixels)
- Avoid time-based interactions or provide alternatives
- Support text resizing up to 200% without loss of functionality

## Documentation Standards
- Document all accessibility features and considerations
- Include usage examples in code comments
- Update README with accessibility information
- Document keyboard shortcuts and navigation patterns

## Security and Privacy
- Protect user location and personal data
- Implement privacy-by-design principles
- Be transparent about data collection and usage
- Follow GDPR and other privacy regulations

## Error Handling
- Provide clear, accessible error messages
- Ensure errors are announced to screen readers
- Offer helpful recovery suggestions
- Log errors appropriately for debugging

## When Suggesting Changes
- Consider the impact on users with disabilities
- Suggest accessible alternatives when proposing UI changes
- Reference WCAG guidelines when relevant
- Think about diverse user needs (blind, low vision, motor impairments, cognitive differences)

## Resources
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Best Practices: https://www.w3.org/WAI/ARIA/apg/
- Inclusive Design Principles: https://inclusivedesignprinciples.org/

## Remember
This project serves people with visual impairments navigating public spaces. Every line of code should honor their dignity, independence, and right to accessible technology.
