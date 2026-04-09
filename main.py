#!/usr/bin/env python3
"""
MotorAssist - Software Adaptation Assistant for Motor Disabilities
Helps users with motor impairments configure their computer for better accessibility.
"""

import sys
import platform
import subprocess

def clear():
      print("\n" * 2)

def ask(question, options):
      print(f"\n{question}")
      for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            while True:
                      try:
                                    choice = int(input("Your choice: "))
                                    if 1 <= choice <= len(options):
                                                      return choice
                      except ValueError:
                                    pass
                                print("Please enter a valid number.")

def apply_windows_settings(profile):
      print("\n  Applying Windows accessibility settings...")
    try:
              if profile["slow_keys"]:
                            subprocess.run([
                                              "reg", "add",
                                              r"HKCU\Control Panel\Accessibility\Keyboard Response",
                                              "/v", "Flags", "/t", "REG_SZ", "/d", "62", "/f"
                            ], check=True)
                            print("  Slow Keys enabled")

        if profile["sticky_keys"]:
                      subprocess.run([
                          "reg", "add",
                          r"HKCU\Control Panel\Accessibility\StickyKeys",
                          "/v", "Flags", "/t", "REG_SZ", "/d", "510", "/f"
        ], check=True)
            print("  Sticky Keys enabled")

        if profile["mouse_speed"] == "slow":
                      subprocess.run([
                          "reg", "add",
                          r"HKCU\Control Panel\Mouse",
                          "/v", "MouseSensitivity", "/t", "REG_SZ", "/d", "3", "/f"
        ], check=True)
            print("  Mouse speed reduced")

        if profile["large_pointer"]:
                      subprocess.run([
                          "reg", "add",
                          r"HKCU\Control Panel\Cursors",
                          "/v", "", "/t", "REG_SZ", "/d", "Windows Aero (extra large)", "/f"
        ], check=True)
            print("  Large mouse pointer set")

except Exception as e:
        print(f"  Could not apply some settings: {e}")
        print("  Try running the script as Administrator.")

def apply_mac_settings(profile):
      print("\n  Applying macOS accessibility settings...")
    try:
              if profile["slow_keys"]:
                            subprocess.run([
                                              "defaults", "write", "com.apple.universalaccess", "slowKey", "-bool", "true"
                            ], check=True)
                            print("  Slow Keys enabled")

        if profile["sticky_keys"]:
                      subprocess.run([
                          "defaults", "write", "com.apple.universalaccess", "stickyKey", "-bool", "true"
        ], check=True)
            print("  Sticky Keys enabled")

        if profile["mouse_speed"] == "slow":
                      subprocess.run([
                          "defaults", "write", "-g", "com.apple.mouse.scaling", "-float", "0.5"
        ], check=True)
            print("  Mouse speed reduced")

        if profile["large_pointer"]:
                      subprocess.run([
                          "defaults", "write", "com.apple.universalaccess", "cursorSize", "-float", "2.5"
        ], check=True)
            print("  Large mouse pointer set")

except Exception as e:
        print(f"  Could not apply some settings: {e}")

def suggest_software(profile):
      print("\n  Recommended software for your profile:\n")
    suggestions = []

    if profile["voice_control"]:
              suggestions.append(("Voice Control",
                                                              "Use your voice to control your computer",
                                                              "Built-in on Windows 11 & macOS - search Voice Access or Voice Control in settings"))
    if profile["one_hand"]:
              suggestions.append(("One-Hand Keyboard Layout",
                                                              "Remap keyboard for one-handed use",
                                                              "https://www.onehandedkeyboard.com/ or KeyTweak (free)"))
    if profile["on_screen_keyboard"]:
              suggestions.append(("On-Screen Keyboard",
                                                              "Virtual keyboard controlled by mouse or eye tracking",
                                                              "Built-in: search On-Screen Keyboard in your OS settings"))
    suggestions.append(("KMouseTool",
                                                "Auto-clicks when mouse stops moving",
                                                "https://apps.kde.org/kmousetool/"))
    suggestions.append(("Talon Voice",
                                                "Advanced voice control for developers",
                                                "https://talonvoice.com/"))

    for name, desc, link in suggestions:
              print(f"  - {name}")
        print(f"     {desc}")
        print(f"     -> {link}\n")

def main():
      print("=" * 55)
    print("  MotorAssist - Motor Disability Setup Assistant")
    print("=" * 55)
    print("\nThis tool helps configure your computer for motor impairments.")
    print("No data is collected. Everything runs locally.\n")

    profile = {}

    q1 = ask("Do you experience tremors or unsteady hand movements?",
                          ["Yes", "No"])
    profile["tremors"] = (q1 == 1)

    q2 = ask("Do you use only one hand to type or control the mouse?",
                          ["Yes", "No"])
    profile["one_hand"] = (q2 == 1)

    q3 = ask("Do you have difficulty pressing multiple keys at the same time?",
                          ["Yes", "No"])
    profile["sticky_keys"] = (q3 == 1)

    q4 = ask("Is the mouse cursor too fast or hard to control?",
                          ["Yes, slow it down", "No, it's fine"])
    profile["mouse_speed"] = "slow" if q4 == 1 else "normal"

    q5 = ask("Would you like a larger mouse pointer?",
                          ["Yes", "No"])
    profile["large_pointer"] = (q5 == 1)

    q6 = ask("Would you like to use voice control?",
                          ["Yes", "No"])
    profile["voice_control"] = (q6 == 1)

    q7 = ask("Would you like an on-screen keyboard?",
                          ["Yes", "No"])
    profile["on_screen_keyboard"] = (q7 == 1)

    profile["slow_keys"] = profile["tremors"]

    os_name = platform.system()
    print(f"\n  Detected OS: {os_name}")

    if os_name == "Windows":
              apply_windows_settings(profile)
elif os_name == "Darwin":
        apply_mac_settings(profile)
else:
        print("  Automatic configuration is not supported on this OS.")
        print("  Please apply settings manually in your system accessibility options.")

    suggest_software(profile)

    print("\n  Setup complete! You may need to restart your session for all changes to take effect.")
    print("=" * 55)

if __name__ == "__main__":
      main()
