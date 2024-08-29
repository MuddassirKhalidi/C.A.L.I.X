import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'asking_button.dart';

class AskingPage extends StatefulWidget {
  final Function(bool) onAskingStateChanged;

  const AskingPage({super.key, required this.onAskingStateChanged});

  @override
  _AskingPageState createState() => _AskingPageState();
}

class _AskingPageState extends State<AskingPage> {
  bool _isAsking = false;

  void _toggleAsking() {
    setState(() {
      _isAsking = !_isAsking;
    });
    widget.onAskingStateChanged(_isAsking);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage('assets/IMG_5482.PNG'),
          fit: BoxFit.cover,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Padding(
            padding: const EdgeInsets.only(
                top: 80.0), // Adjust the padding as needed
            child: Text(
              'Recall',
              style: GoogleFonts.robotoMono(
                textStyle: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Color.fromARGB(255, 219, 197, 255),
                ),
              ),
            ),
          ),
          Center(
            child: AskingButton(
              isAsking: _isAsking,
              onTap: _toggleAsking,
            ),
          ),
          const SizedBox(height: 40), // Extra spacing at the bottom if needed
        ],
      ),
    );
  }
}
