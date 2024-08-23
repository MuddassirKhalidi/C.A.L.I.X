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

  void _onItemTapped(int index) {
    if (_isRecording || _isAsking) return;
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: _pages,
      ),
      bottomNavigationBar: MotionTabBar(
        tabBarColor: const Color(0xFF160239),
        labels: const ["Home", "Record", "Ask"],
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
          setState(() {
            _selectedIndex = index;
          });
        },
      ),
    );
  }
}
