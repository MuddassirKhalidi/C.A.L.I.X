import 'package:flutter/material.dart';
import 'package:aida_app/AskingPage.dart'; // Import the next page
import 'package:aida_app/IntroductionPage.dart'; // Import the Introduction page
import 'package:aida_app/recordingButton.dart'; // Import your custom recording button

class RecordingPage extends StatefulWidget {
  @override
  _RecordingPageState createState() => _RecordingPageState();
}

class _RecordingPageState extends State<RecordingPage> {
  bool _isRecording = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        title: Center(
          child: Text(
            "Record conversation",
            style: TextStyle(
              fontSize: 24,
              color: Color(0xFF6A0DAD),
              fontFamily: 'OpenSans',
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        elevation: 0, // Remove shadow from AppBar
        leading: IconButton(
          icon: Icon(Icons.menu, color: Color(0xFF6A0DAD)),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => IntroductionPage()),
            );
          },
        ),
      ),
      extendBodyBehindAppBar: true, // Extend body behind AppBar
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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Spacer(), // Push the recording button to the center
            RecordingButton(
              isRecording: _isRecording,
              onTap: () {
                setState(() {
                  _isRecording = !_isRecording;
                });
              },
            ),
            Spacer(), // Push the navigation button to the bottom
            Padding(
              padding:
                  const EdgeInsets.only(bottom: 50.0), // Add padding if needed
              child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => AskingPage()),
                  );
                },
                child: Text(
                  "Asking Page",
                  style: TextStyle(
                    color: Color.fromARGB(255, 203, 197, 208),
                  ),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color.fromARGB(255, 171, 60, 255),
                  padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  textStyle: TextStyle(
                    fontSize: 20,
                    fontFamily: 'OpenSans',
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
