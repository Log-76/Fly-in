_This project has been created as part of the 42 curriculum by \[lleriche\]._

Fly-in
======

Description
-----------

**Fly-in** is a high-performance drone fleet simulation engine designed to coordinate multiple autonomous drones through a network of hubs and links. The project's core challenge is to optimize the movement of drones from their starting positions to their targets in a minimum number of turns (aiming for a 45-turn benchmark) while strictly adhering to zone capacity constraints. The system ensures a completely deadlock-free environment, managing complex traffic flow within a graph-based infrastructure.

Instructions
------------

### Installation

This project uses Python 3.10+. No external dependencies are required as it relies solely on the Python Standard Library.

1.  git clone \[your\_repository\_url\]cd Fly-in
    

### Execution

To launch the simulation with a specific map file, provide the path as a command-line argument:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python3 Fly_in.py maps/easy/01_linear_path.txt   `

### Development & Quality Control

The project maintains high coding standards. To verify type consistency and code quality using Mypy:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   mypy .   `

Algorithm & Implementation Strategy
-----------------------------------

### Pathfinding: Adaptive Dijkstra

The navigation core is powered by a **Dynamic Dijkstra Algorithm**. Unlike a static pathfinder, this implementation evaluates the cost of movement in real-time to adapt to changing network conditions:

*   **Turn-Based Optimization:** The cost function treats each connection as a unit of time, ensuring drones prioritize paths that minimize the total turn count.
    
*   **Wait-and-Recalculate Logic:** To prevent permanent congestion, the system monitors "stall turns." If a drone is blocked for **2 consecutive turns** due to hub capacity limits, the algorithm triggers a full path recalculation. This allows drones to pivot to alternative routes if the primary path remains saturated.
    
*   **Priority Zone Awareness:** The cost function is weighted to account for priority zones, ensuring that the overall flow of the swarm remains fluid even in high-density areas of the map.
    

### Deadlock Prevention

Deadlocks are strictly mitigated through a "Capacity-First" protocol. A drone will only move to the next hub if the destination has available space (max\_drones). Combined with the 2-turn recalculation rule, this ensures that the simulation never enters a permanent stall, as drones will eventually seek different paths rather than creating circular blockages.

Visual Representation
---------------------

To enhance the user experience and facilitate real-time monitoring of complex fleet movements, **Fly-in** implements a sophisticated terminal-based visualization system using ANSI escape codes:

*   **Strategic Color Coding:**
    
    *   **Gold & Green:** Highlight target hubs and successful mission completions for immediate visual confirmation.
        
    *   **Lime:** Represents optimal paths and available zones, standing out clearly against the terminal background.
        
    *   **Crimson & Dark Red:** Indicate critical traffic areas or hubs at maximum capacity.
        
    *   **Violet & Purple:** Distinguish specific priority zones and intermediary waypoints.
        
*   **Rainbow Effect:** A dynamic color-cycling animation is applied to high-priority events or mission-critical hubs, drawing the user's attention to key focal points.
    
*   **UX Impact:** This system transforms raw log data into an intuitive visual dashboard. Users can immediately identify bottlenecks, "breathing" patterns in the traffic, and successful flow resolutions without manually parsing thousands of lines of text logs.
    

Resources & AI Use
------------------

### Classic References

*   **Graph Theory:** Standard documentation on Dijkstra's Algorithm for shortest path calculations.
    
*   **ANSI Standards:** Technical references for 8-bit color rendering in Unix-based terminals.
    

### AI Attribution

AI (Gemini) was utilized as a collaborative tool for the following specific tasks:

*   **Visual System Implementation:** Assisted in mapping specific color names to their respective 8-bit ANSI codes and developing the logic for the dynamic rainbow string iterator.
    
*   **Documentation:** Assisted in structuring and translating the technical specifications into this English README to ensure compliance with the 42 curriculum standards.