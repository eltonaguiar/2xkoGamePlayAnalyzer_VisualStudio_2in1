"""
Video Analysis Engine
Processes MP4 files and detects game events
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
import os


class VideoFrameAnalyzer:
    """Analyzes video frames for fighting game data"""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None
        self.fps = 0
        self.total_frames = 0
        self.frame_data_history = []
        
    def open_video(self) -> bool:
        """Open video file"""
        if not os.path.exists(self.video_path):
            print(f"Error: Video file not found: {self.video_path}")
            return False
            
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print(f"Error: Could not open video: {self.video_path}")
            return False
            
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Video opened: {self.total_frames} frames @ {self.fps} FPS")
        return True
    
    def get_video_duration(self) -> float:
        """Get video duration in seconds"""
        if self.total_frames == 0 or self.fps == 0:
            return 0
        return self.total_frames / self.fps
    
    def get_timestamp(self, frame_number: int) -> str:
        """Convert frame number to MM:SS:FF timestamp"""
        if self.fps == 0:
            return "00:00:00"
        
        total_seconds = frame_number / self.fps
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        frames = int((total_seconds * self.fps) % self.fps)
        
        return f"{minutes:02d}:{seconds:02d}:{frames:02d}"
    
    def get_frame_at(self, frame_number: int) -> Optional[np.ndarray]:
        """Get specific frame"""
        if self.cap is None:
            return None
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def extract_frames_segment(self, start_frame: int, end_frame: int, step: int = 1):
        """Extract frames in a range"""
        if self.cap is None:
            return []
        
        frames = []
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for frame_num in range(start_frame, end_frame, step):
            ret, frame = self.cap.read()
            if ret:
                frames.append((frame_num, frame))
            else:
                break
        
        return frames
    
    def detect_color_regions(self, frame: np.ndarray, color_range: Tuple) -> np.ndarray:
        """Detect regions of specific color (HSV)"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower, upper = color_range
        mask = cv2.inRange(hsv, lower, upper)
        return mask
    
    def get_frame_brightness(self, frame: np.ndarray) -> float:
        """Calculate average brightness of frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.mean(gray)
    
    def detect_screen_flash(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: int = 50) -> bool:
        """Detect if a screen flash occurred (super/ultimate activation)"""
        if prev_frame is None:
            return False
        
        prev_brightness = self.get_frame_brightness(prev_frame)
        curr_brightness = self.get_frame_brightness(curr_frame)
        
        return abs(curr_brightness - prev_brightness) > threshold
    
    def detect_motion(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> float:
        """Detect motion between frames (optical flow magnitude)"""
        if prev_frame is None or curr_frame is None:
            return 0.0
        
        gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray_curr = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        flow = cv2.calcOpticalFlowFarneback(
            gray_prev, gray_curr, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )
        
        magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
        return np.mean(magnitude)
    
    def close(self):
        """Close video file"""
        if self.cap:
            self.cap.release()
    
    def extract_video_clip(self, start_frame: int, end_frame: int, output_path: str, quality: int = 20):
        """Extract video frames as a GIF preview (animated replay)
        
        Creates an animated GIF showing the mistake in action
        Args:
            start_frame: Starting frame number
            end_frame: Ending frame number
            output_path: Path to save the GIF file (will use .gif extension)
            quality: Quality level (1-100)
        
        Returns:
            Path to created GIF file if successful, empty string otherwise
        """
        try:
            from PIL import Image
        except ImportError:
            print(f"⚠ PIL/Pillow not available - skipping GIF generation")
            return ""
        
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            # Create a fresh video reader for extraction (don't modify self.cap)
            temp_cap = cv2.VideoCapture(self.video_path)
            if not temp_cap.isOpened():
                print(f"✗ Could not open video for clip extraction")
                return ""
            
            frames = []
            frame_count = 0
            # Target ~15 frames in GIF for smaller file size (was 30)
            step = max(1, (end_frame - start_frame) // 15)
            
            for frame_num in range(start_frame, min(end_frame, int(self.total_frames)), step):
                # Set position and read frame
                temp_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = temp_cap.read()
                if not ret:
                    break
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Aggressive resize for web - 30% of original
                height, width = rgb_frame.shape[:2]
                scale = 0.3  # 30% of original (was 50%)
                new_width = int(width * scale)
                new_height = int(height * scale)
                resized = cv2.resize(rgb_frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                # Convert to PIL Image and reduce colors for compression
                pil_frame = Image.fromarray(resized)
                # Convert to RGB mode with reduced palette (256 colors)
                pil_frame = pil_frame.quantize(colors=256)
                frames.append(pil_frame)
                frame_count += 1
            
            temp_cap.release()
            
            # Save as GIF with heavy optimization
            if frames and frame_count > 2:
                output_gif = output_path.replace('.mp4', '.gif')
                try:
                    frames[0].save(
                        output_gif,
                        save_all=True,
                        append_images=frames[1:],
                        duration=150,  # 150ms per frame (slower playback for smaller files)
                        loop=0,  # Loop infinitely
                        optimize=True,  # Enable optimization (quantize helps too)
                        quality=95  # PIL's quality parameter
                    )
                    
                    if os.path.exists(output_gif) and os.path.getsize(output_gif) > 10000:
                        size_kb = os.path.getsize(output_gif) / 1024
                        print(f"✓ Extracted replay: {os.path.basename(output_gif)} ({frame_count} frames, {size_kb:.0f}KB)")
                        
                        # Also create MP4 version for better speed control
                        self._create_mp4_from_frames(start_frame, end_frame, output_path)
                        
                        return output_gif
                    elif os.path.exists(output_gif):
                        print(f"⚠ GIF too small: {os.path.basename(output_gif)} ({os.path.getsize(output_gif)} bytes)")
                        return ""
                except Exception as e:
                    print(f"✗ Error saving GIF: {e}")
                    return ""
            
            return ""
                
        except Exception as e:
            print(f"✗ Error extracting clip: {e}")
            return ""
    
    def _create_mp4_from_frames(self, start_frame: int, end_frame: int, output_path: str):
        """Create MP4 video file from frames for better speed control
        
        Args:
            start_frame: Starting frame number
            end_frame: Ending frame number
            output_path: Path to save the MP4 file
        """
        try:
            temp_cap = cv2.VideoCapture(self.video_path)
            if not temp_cap.isOpened():
                return
            
            # Get video properties
            fps = self.fps
            width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.3)  # 30% of original
            height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.3)
            
            # Create video writer for MP4
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_mp4 = output_path.replace('.gif', '.mp4')
            writer = cv2.VideoWriter(output_mp4, fourcc, fps, (width, height))
            
            frame_count = 0
            for frame_num in range(start_frame, min(end_frame, int(self.total_frames))):
                temp_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = temp_cap.read()
                if not ret:
                    break
                
                # Resize frame
                resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
                writer.write(resized)
                frame_count += 1
            
            writer.release()
            temp_cap.release()
            
            if os.path.exists(output_mp4):
                size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
                if size_mb > 0.1:  # Only keep if > 100KB
                    print(f"✓ Created MP4 replay: {os.path.basename(output_mp4)} ({frame_count} frames, {size_mb:.2f}MB)")
        except Exception as e:
            print(f"⚠ MP4 creation skipped: {e}")


class GameStateDetector:
    """Detects game states from video frames"""
    
    def __init__(self, analyzer: VideoFrameAnalyzer):
        self.analyzer = analyzer
        self.round_starts = []
        self.hits_detected = []
        self.blockstrings = []
        
    def detect_hit_flash(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> bool:
        """Detect hit impact flash"""
        # Look for sudden brightness change indicating hit
        if self.analyzer.detect_screen_flash(prev_frame, curr_frame, threshold=40):
            # Further verification: check for motion
            motion = self.analyzer.detect_motion(prev_frame, curr_frame)
            return motion > 5  # Threshold for significant motion
        return False
    
    def scan_video_for_events(self, start_frame: int = 0, end_frame: Optional[int] = None, sample_rate: int = 2):
        """Scan entire video for game events"""
        if end_frame is None:
            end_frame = self.analyzer.total_frames
        
        events = []
        prev_frame = None
        prev_brightness = 0
        
        self.analyzer.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for frame_num in range(start_frame, end_frame, sample_rate):
            ret, frame = self.analyzer.cap.read()
            if not ret:
                break
            
            # Detect flashes and motion
            brightness = self.analyzer.get_frame_brightness(frame)
            flash_detected = self.detect_hit_flash(prev_frame, frame) if prev_frame is not None else False
            
            if flash_detected:
                timestamp = self.analyzer.get_timestamp(frame_num)
                events.append({
                    "type": "potential_hit",
                    "frame": frame_num,
                    "timestamp": timestamp,
                    "confidence": 0.6
                })
            
            prev_frame = frame
            prev_brightness = brightness
        
        return events


class MoveDetector:
    """Detects character moves from game state"""
    
    def __init__(self):
        self.move_startup_durations = {}
        self.move_recovery_durations = {}
        
    def estimate_move_from_duration(self, duration_frames: int, fps: int) -> Dict:
        """Estimate which move was performed based on frame duration"""
        # This is a simplified heuristic - in production would use more sophisticated ML
        
        if duration_frames < 10:
            return {"type": "normal", "speed": "fast"}
        elif duration_frames < 20:
            return {"type": "normal", "speed": "medium"}
        elif duration_frames < 30:
            return {"type": "special", "speed": "slow"}
        else:
            return {"type": "special", "speed": "very_slow"}


class AnalysisSession:
    """Manages a complete analysis session"""
    
    def __init__(self, video_path: str, character1: str = "Blitzcrank", character2: str = "Blitzcrank", mode: str = "Juggernaut"):
        self.video_path = video_path
        self.character1 = character1
        self.character2 = character2
        self.mode = mode
        self.analyzer = VideoFrameAnalyzer(video_path)
        self.detector = GameStateDetector(self.analyzer)
        self.move_detector = MoveDetector()
        self.events = []
        
    def analyze(self) -> bool:
        """Run full analysis"""
        if not self.analyzer.open_video():
            return False
        
        print(f"\n{'='*60}")
        print(f"2XKO GAMEPLAY ANALYSIS")
        print(f"{'='*60}")
        print(f"Character 1: {self.character1}")
        print(f"Character 2: {self.character2}")
        print(f"Mode: {self.mode}")
        print(f"Video: {self.video_path}")
        print(f"Duration: {self.analyzer.get_video_duration():.2f} seconds")
        print(f"FPS: {self.analyzer.fps}")
        print(f"{'='*60}\n")
        
        # Scan for events
        print("Scanning video for gameplay events...")
        self.events = self.detector.scan_video_for_events(sample_rate=5)
        print(f"Found {len(self.events)} potential events\n")
        
        self.analyzer.close()
        return True
