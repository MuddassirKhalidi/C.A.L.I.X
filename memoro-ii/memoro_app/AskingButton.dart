// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';

class AskingButton extends StatelessWidget {
  final bool isAsking;
  final VoidCallback onTap;

  const AskingButton({required this.isAsking, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: onTap,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 120,
              height: 120,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isAsking
                    ? Colors.red
                    : const Color.fromARGB(255, 39, 176, 92),
                boxShadow: [
                  BoxShadow(
                    offset: Offset(0, 15),
                    blurRadius: 25,
                    color: const Color.fromARGB(186, 0, 0, 0),
                  ),
                ],
              ),
              child: Icon(
                isAsking ? Icons.stop : Icons.mic,
                size: 60,
                color: Color.fromARGB(255, 203, 197, 208),
              ),
            ),
            SizedBox(width: 16),
            Text(
              isAsking ? 'Finish Asking' : 'Click to Start Asking',
              style: TextStyle(
                fontSize: 18,
                fontFamily: 'OpenSans',
                fontWeight: FontWeight.bold,
                color: Color.fromARGB(255, 203, 197, 208),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
