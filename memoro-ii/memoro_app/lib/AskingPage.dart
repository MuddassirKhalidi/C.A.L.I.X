import 'package:flutter/material.dart';
import 'package:memoro_app3/IntroductionPage.dart';
import 'package:memoro_app3/RecordingPage.dart';
import 'package:memoro_app3/askingButton.dart'; // Import your custom asking button

class AskingPage extends StatefulWidget {
  @override
  _AskingPageState createState() => _AskingPageState();
}

class _AskingPageState extends State<AskingPage> {
  bool _isAsking = false;

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
        elevation: 0, // Removes the shadow
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
      extendBodyBehindAppBar: true, // Extends the gradient behind the AppBar
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
            Spacer(), // Pushes the AskingButton to the center
            AskingButton(
              isAsking: _isAsking,
              onTap: () {
                setState(() {
                  _isAsking = !_isAsking;
                });
              },
            ),
            Spacer(), // Pushes the ElevatedButton to the bottom
            Padding(
              padding: const EdgeInsets.only(
                  bottom: 50.0), // Optional: Add padding if needed
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
