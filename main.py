"""
2XKO Gameplay Analysis Tool - Main Entry Point
Analyzes fighting game footage from 2XKO (2v2 FT)
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_analyzer import AnalysisSession
from analysis_engine import AnalysisReport, PlaystyleAnalyzer, RecommendationEngine
from frame_data import BLITZCRANK_FRAME_DATA, get_frame_data


class GameplayAnalyzer:
    """Main analyzer orchestrator"""
    
    def __init__(self):
        self.session: Optional[AnalysisSession] = None
        self.report: Optional[AnalysisReport] = None
        self.character_list = ["Blitzcrank", "Ahri", "Braum", "Darius", "Ekko", 
                              "Illaoi", "Jinx", "Teemo", "Vi", "Warwick", "Yasuo"]
        self.modes = ["Juggernaut", "Standard"]
        
    def print_header(self):
        """Print application header"""
        header = """
        ╔════════════════════════════════════════════════════════╗
        ║          2XKO GAMEPLAY ANALYZER v1.0                    ║
        ║                                                         ║
        ║  Analyze fighting game footage & get improvement tips   ║
        ║  Focus: Frame Data, Mistakes, Playstyle Analysis       ║
        ╚════════════════════════════════════════════════════════╝
        """
        print(header)
    
    def print_menu(self):
        """Print main menu"""
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Analyze Gameplay Video")
        print("2. View Available Characters")
        print("3. View Blitzcrank Frame Data")
        print("4. View Blitzcrank Tips")
        print("5. Exit")
        print("-"*60)
    
    def select_character(self, player_num: int) -> str:
        """Character selection menu"""
        print(f"\nSelect Character for Player {player_num}:")
        print("-" * 40)
        for i, char in enumerate(self.character_list, 1):
            print(f"{i:2d}. {char}")
        print("0.  Back")
        print("-" * 40)
        
        while True:
            try:
                choice = int(input(f"Enter choice (1-{len(self.character_list)}): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(self.character_list):
                    return self.character_list[choice - 1]
                print("Invalid choice!")
            except ValueError:
                print("Please enter a number")
    
    def select_mode(self) -> str:
        """Mode selection menu"""
        print("\nSelect Game Mode:")
        print("-" * 40)
        for i, mode in enumerate(self.modes, 1):
            print(f"{i}. {mode}")
        print("0. Back")
        print("-" * 40)
        
        while True:
            try:
                choice = int(input(f"Enter choice (1-{len(self.modes)}): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(self.modes):
                    return self.modes[choice - 1]
                print("Invalid choice!")
            except ValueError:
                print("Please enter a number")
    
    def get_video_path(self) -> Optional[str]:
        """Get video file from user"""
        print("\n" + "="*60)
        print("SELECT VIDEO FILE")
        print("="*60)
        
        # Check for default location first
        desktop_path = Path.home() / "Desktop"
        default_video = desktop_path / "2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4"
        
        if default_video.exists():
            print(f"Found video at default location:")
            print(f"  {default_video}")
            use_default = input("Use this file? (y/n): ").lower()
            if use_default == 'y':
                return str(default_video)
        
        # Get custom path
        print("\nEnter video file path:")
        print("(Can be absolute or relative path)")
        path = input("> ").strip('"')  # Remove quotes if pasted
        
        if os.path.exists(path):
            return os.path.abspath(path)
        else:
            print(f"Error: File not found: {path}")
            return None
    
    def analyze_video(self):
        """Run video analysis workflow"""
        print("\n" + "="*60)
        print("GAMEPLAY ANALYSIS")
        print("="*60)
        
        # Get video
        video_path = self.get_video_path()
        if not video_path:
            return
        
        # Get characters
        char1 = self.select_character(1)
        if not char1:
            return
        
        char2 = self.select_character(2)
        if not char2:
            return
        
        # Get mode
        mode = self.select_mode()
        if not mode:
            return
        
        # Create and run analysis
        print("\nStarting analysis...")
        self.session = AnalysisSession(video_path, char1, char2, mode)
        
        if not self.session.analyze():
            print("Analysis failed!")
            return
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate and display analysis report"""
        if not self.session:
            return
        
        self.report = AnalysisReport()
        
        # In a real implementation, this would be populated with actual analysis
        # For now, we'll show the framework
        
        print("\n" + "="*60)
        print("ANALYSIS REPORT")
        print("="*60)
        
        # Show video info
        print(f"\nVideo Information:")
        print(f"  Characters: {self.session.character1} vs {self.session.character2}")
        print(f"  Mode: {self.session.mode}")
        print(f"  Duration: {self.session.analyzer.get_video_duration():.2f} seconds")
        print(f"  FPS: {self.session.analyzer.fps}")
        
        # Show detected events
        print(f"\nDetected Events:")
        print(f"  Total events: {len(self.session.events)}")
        for event in self.session.events[:5]:  # Show first 5
            print(f"    [{event['timestamp']}] {event['type']} (confidence: {event['confidence']:.0%})")
        
        # Show recommendations
        print(self.show_blitzcrank_analysis())
        
        # Export option
        export = input("\nExport analysis to JSON? (y/n): ").lower()
        if export == 'y':
            output_path = "output/analysis_report.json"
            os.makedirs("output", exist_ok=True)
            self.report.export_json(output_path)
    
    def show_blitzcrank_analysis(self) -> str:
        """Show Blitzcrank-specific analysis"""
        tips = RecommendationEngine.get_blitzcrank_tips()
        
        analysis = "\n" + "="*60
        analysis += "\nBLITZCRANK ANALYSIS & TIPS\n"
        analysis += "="*60 + "\n"
        
        analysis += "\n🎮 NEUTRAL GAME TIPS:\n"
        for tip in tips["neutral_game"]:
            analysis += f"  • {tip}\n"
        
        analysis += "\n🔄 MIX-UP GAME:\n"
        for tip in tips["mixup_game"]:
            analysis += f"  • {tip}\n"
        
        analysis += "\n⚔️ NEUTRAL TOOLS:\n"
        for tip in tips["neutral_tools"]:
            analysis += f"  • {tip}\n"
        
        analysis += "\n💨 STEAM MECHANIC:\n"
        for tip in tips["steam_mechanic"]:
            analysis += f"  • {tip}\n"
        
        analysis += "\n🏆 MIRROR MATCHUP TIPS:\n"
        for tip in tips["matchup_tips_blitzcrank_mirror"]:
            analysis += f"  • {tip}\n"
        
        return analysis
    
    def show_frame_data(self):
        """Display Blitzcrank frame data"""
        print("\n" + "="*60)
        print("BLITZCRANK FRAME DATA")
        print("="*60)
        
        categories = {
            "Standing Normals": ["5L", "5M", "5H", "5H_charged"],
            "Crouching Normals": ["2L", "2M", "2H"],
            "Jumping Normals": ["jL", "jM", "jH", "j2H"],
            "Specials": ["5S1", "5S1_steam", "2S1", "2S1_steam", "2S2", "6S2", "jS1"],
            "Throws": ["5MH", "4MH", "jMH"],
        }
        
        print("\nSelect category to view:")
        print("-" * 40)
        cat_list = list(categories.keys())
        for i, cat in enumerate(cat_list, 1):
            print(f"{i}. {cat}")
        print(f"{len(cat_list)+1}. Search Move")
        print("0. Back")
        print("-" * 40)
        
        try:
            choice = int(input("Enter choice: "))
            if choice == 0:
                return
            elif choice == len(cat_list) + 1:
                self.search_move()
            elif 1 <= choice <= len(cat_list):
                self.display_category(cat_list[choice-1], categories)
        except ValueError:
            print("Invalid input")
    
    def display_category(self, category: str, categories: dict):
        """Display moves in a category"""
        print(f"\n{category}")
        print("-" * 60)
        
        for move in categories[category]:
            data = get_frame_data(move)
            if data:
                print(f"\n{move:12} | Damage: {data.get('damage', '—'):4} | "
                      f"Startup: {data.get('startup', '—'):3}f | "
                      f"Recovery: {data.get('recovery', '—'):3}f | "
                      f"Block: {data.get('on_block', '—'):+3}f")
                print(f"             Description: {data.get('description', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def search_move(self):
        """Search for a specific move"""
        print("\nSearch for move (e.g., '5L', '2H', 'Rocket Grab'):")
        query = input("> ").strip()
        
        results = [move for move in BLITZCRANK_FRAME_DATA.keys() 
                  if query.lower() in move.lower()]
        
        if not results:
            print("No moves found!")
            return
        
        print(f"\nFound {len(results)} move(s):")
        print("-" * 60)
        
        for move in results:
            data = get_frame_data(move)
            if data:
                safe = "✓ SAFE" if data.get('on_block', -999) >= 0 else f"✗ UNSAFE ({data.get('on_block')}f)"
                print(f"\n{move}")
                print(f"  Damage: {data.get('damage')} | Startup: {data.get('startup')}f | "
                      f"Recovery: {data.get('recovery')}f")
                print(f"  On Block: {safe}")
                print(f"  Description: {data.get('description', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def show_characters(self):
        """List available characters"""
        print("\n" + "="*60)
        print("AVAILABLE CHARACTERS")
        print("="*60)
        
        for i, char in enumerate(self.character_list, 1):
            status = "✓ Frame data available" if char == "Blitzcrank" else "Frame data coming soon..."
            print(f"{i:2d}. {char:15} - {status}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        self.print_header()
        
        while True:
            self.print_menu()
            
            try:
                choice = input("Enter choice: ").strip()
                
                if choice == "1":
                    self.analyze_video()
                elif choice == "2":
                    self.show_characters()
                elif choice == "3":
                    self.show_frame_data()
                elif choice == "4":
                    tips = RecommendationEngine.get_blitzcrank_tips()
                    print(self.show_blitzcrank_analysis())
                    input("Press Enter to continue...")
                elif choice == "5":
                    print("\nThank you for using 2XKO Analyzer!")
                    break
                else:
                    print("Invalid choice!")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Application entry point"""
    analyzer = GameplayAnalyzer()
    analyzer.run()


if __name__ == "__main__":
    main()
