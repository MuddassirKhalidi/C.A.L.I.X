import 'package:flutter/material.dart';
import 'package:memoro_app/IntroductionPage.dart';
import 'package:memoro_app/RecordingPage.dart';
import 'package:memoro_app/askingButton.dart'; // Import your custom asking button
import 'package:http/http.dart' as http;

class AskingPage extends StatefulWidget {
  @override
  _AskingPageState createState() => _AskingPageState();
}

class _AskingPageState extends State<AskingPage> {
  bool _isAsking = false;

  Future<void> startAsking() async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/listen'),
    );

    if (response.statusCode == 200) {
      print('Asking started');
    } else {
      print('Failed to start asking');
    }
  }

  Future<void> stopAsking() async {
    final stopResponse = await http.post(
      Uri.parse('http://127.0.0.1:5000/stop_listening'),
    );

    if (stopResponse.statusCode == 200) {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/generate_response'),
      );

      if (response.statusCode == 200) {
        print('Response generated');
      } else {
        print('Failed to generate response');
      }
    } else {
      print('Failed to stop asking');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(
          child: Text(
            "Asking",
            style: TextStyle(
              fontSize: 24,
              color: const Color.fromARGB(255, 97, 1, 114),
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
            AskingButton(
              isAsking: _isAsking,
              onTap: () async {
                if (_isAsking) {
                  await stopAsking();
                } else {
                  await startAsking();
                }
                setState(() {
                  _isAsking = !_isAsking;
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
                    MaterialPageRoute(builder: (context) => RecordingPage()),
                  );
                },
                child: Text(
                  "Recording Page",
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