# AngelAutomates- (Navarro Mission Control)

Flutter app — `navarro_mission_control`. Early-stage, multi-platform (Android,
iOS, macOS, Windows, Linux, Web).

## Essential commands

```bash
flutter pub get          # install dependencies
flutter analyze          # lint (must pass before merge)
flutter test             # run tests (must pass before merge)
flutter run              # launch on connected device / emulator
```

CI runs `flutter analyze` + `flutter test` on every PR to `main`.

## Stack

- Flutter stable / Dart 3.11.4+
- No third-party state management yet (plain `setState`)
- No backend yet
- Material Design 3, seed color `Colors.deepPurple`

## File map

```
lib/
  main.dart              # MyApp + MyHomePage counter widget (template)
test/
  widget_test.dart       # counter smoke test
.github/
  workflows/
    flutter-ci.yml       # analyze + test on push/PR to main
.claude/
  commands/
    goal.md              # /goal — long-horizon objective with verify loop
    sprint.md            # /sprint — ordered batch of /goal-style objectives
  goals/
    current.json         # active /goal state (created at runtime)
    sprint.json          # active /sprint state (created at runtime)
```

## Development conventions

- All Dart code must pass `flutter analyze` with zero issues
- Use Material 3 widgets; keep the deep purple seed color unless explicitly
  changing the theme
- Write widget tests for any new screen added to `lib/`

## Long-horizon agent commands

Use `/goal` when you want me to pursue a single verifiable objective across
multiple turns (plan → act → verify loop). Use `/sprint` for an ordered set
of 2–5 related goals.

```
/goal Migrate counter to Riverpod AsyncValue, keep flutter test green
/goal check
/goal continue
/goal done | /goal clear

/sprint v0.1 -- Add login screen | Add home dashboard | Write widget tests
/sprint next
/sprint status
/sprint clear
```

State is persisted in `.claude/goals/` between turns.
