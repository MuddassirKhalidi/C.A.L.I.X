import 'package:flutter/material.dart';
import 'package:memoro_app/AskingPage.dart'; // Import the next page
import 'package:memoro_app/IntroductionPage.dart'; // Import the Introduction page
import 'package:memoro_app/recordingButton.dart'; // Import your custom recording button
import 'package:http/http.dart' as http;

class RecordingPage extends StatefulWidget {
  @override
  _RecordingPageState createState() => _RecordingPageState();
}

class _RecordingPageState extends State<RecordingPage> {
  bool _isRecording = false;

  Future<void> startRecording() async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/listen'),
    );

    if (response.statusCode == 200) {
      print('Recording started');
    } else {
      print('Failed to start recording');
    }
  }

  Future<void> stopRecording() async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/stop_listening'),
    );

    if (response.statusCode == 200) {
      print('Recording stopped');
    } else {
      print('Failed to stop recording');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
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
        backgroundColor: Colors.white,
        elevation: 0,
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
      extendBodyBehindAppBar: true,
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
            Spacer(),
            RecordingButton(
              isRecording: _isRecording,
              onTap: () async {
                if (_isRecording) {
                  await stopRecording();
                } else {
                  await startRecording();
                }
                setState(() {
                  _isRecording = !_isRecording;
                });
              },
            ),
            Spacer(),
            Padding(
              padding: const EdgeInsets.only(bottom: 50.0),
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