import 'package:flutter/material.dart';
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
        gradient: LinearGradient(
          colors: [
            Color(0xFF000000),
            Color(0xFF300063),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Center(
        child: AskingButton(
          isAsking: _isAsking,
          onTap: _toggleAsking,
        ),
      ),
    );
  }
}
