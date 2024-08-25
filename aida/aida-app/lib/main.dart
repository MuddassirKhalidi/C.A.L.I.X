import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:motion_tab_bar/MotionTabBar.dart';
import 'home_page.dart';
import 'recording_page.dart';
import 'asking_page.dart';

void main() {
  runApp(const AIDA());
}

class AIDA extends StatelessWidget {
  const AIDA({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AIDA',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: const MainPage(),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  bool _isRecording = false;
  bool _isAsking = false;

  late List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    _pages = [
      const HomePage(),
      RecordingPage(
        onRecordingStateChanged: (isRecording) {
          setState(() {
            _isRecording = isRecording;
          });
        },
      ),
      AskingPage(
        onAskingStateChanged: (isAsking) {
          setState(() {
            _isAsking = isAsking;
          });
        },
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: _pages,
      ),
      bottomNavigationBar: GestureDetector(
        onTap: () {
          if (_isRecording || _isAsking) {
            // Show a message or perform any action if needed
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  'Please stop recording or asking before navigating.',
                  style: GoogleFonts.robotoMono(),
                ),
              ),
            );
          }
        },
        child: AbsorbPointer(
          absorbing: _isRecording ||
              _isAsking, // Disable interaction when recording or asking
          child: MotionTabBar(
            tabBarColor: const Color(0xFF160239),
            labels: const ["Home", "Record", "Recall"],
            initialSelectedTab: "Home",
            tabIconColor: const Color.fromARGB(255, 219, 197, 255),
            tabSelectedColor: const Color(0xFFC75DEE),
            textStyle: GoogleFonts.robotoMono(
              textStyle: const TextStyle(
                color: Color.fromARGB(255, 243, 236, 236),
                fontSize: 15,
                fontWeight: FontWeight.bold,
              ),
            ),
            icons: const [Icons.home, Icons.mic, Icons.question_answer],
            onTabItemSelected: (int index) {
              if (_isRecording || _isAsking) {
                // Prevent changing tabs while recording or asking
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      'Please stop recording or asking before navigating.',
                      style: GoogleFonts.robotoMono(),
                    ),
                  ),
                );
                return;
              }
              setState(() {
                _selectedIndex = index;
              });
            },
          ),
        ),
      ),
    );
  }
}
