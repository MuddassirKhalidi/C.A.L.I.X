import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:memoro_app3/RecordingPage.dart'; // Import the next page

class IntroductionPage extends StatefulWidget {
  @override
  _IntroductionPageState createState() => _IntroductionPageState();
}

class _IntroductionPageState extends State<IntroductionPage> {
  late AudioPlayer _audioPlayer;

  @override
  void initState() {
    super.initState();
    _audioPlayer = AudioPlayer();
    _playBackgroundMusic();
  }

  void _playBackgroundMusic() async {
    await _audioPlayer.play(AssetSource('background_music.mp3'),
        volume: 0.5); // Adjust volume as needed
  }

  @override
  void dispose() {
    _audioPlayer
        .dispose(); // Dispose the audio player when the page is destroyed
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            "Welcome to AIDA",
            style: TextStyle(
              fontSize: 24,
              color: const Color.fromARGB(255, 97, 1, 114),
              fontFamily: 'OpenSans',
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0, // Remove AppBar shadow
        automaticallyImplyLeading: false, // This removes the back arrow
      ),
      extendBodyBehindAppBar: true, // Extend the body behind the AppBar
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color.fromARGB(255, 0, 0, 0),
              Color.fromARGB(255, 48, 0, 99),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                "Welcome to AIDA!",
                style: TextStyle(
                  fontSize: 24,
                  color: Color.fromARGB(255, 203, 197, 208),
                  fontFamily: 'OpenSans',
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 20),
              Text(
                "Click the button below to start using the app.",
                style: TextStyle(
                  fontSize: 18,
                  color: Color.fromARGB(255, 203, 197, 208),
                  fontFamily: 'OpenSans',
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 50),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => RecordingPage()),
                  );
                },
                child: Text(
                  "Get Started",
                  style: TextStyle(
                    color: Color.fromARGB(255, 203, 197, 208),
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color.fromARGB(
                      255, 171, 60, 255), // Button background color
                  padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  textStyle: TextStyle(
                    fontSize: 20,
                    fontFamily: 'OpenSans',
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
