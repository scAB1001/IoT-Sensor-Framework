1. Title
A concise title that accurately describes the subject of your project.
The subject should be the computer science problem that you are investigating.
It should not be, for example, a software artefact(e.g. a mobile app or web site) – that is a
Deliverable of the project, and part of your solution, but not the subject.

*Replacing Joystick Control: A Hand-Gesture Based Navigation System for 3D Anatomy Manipulation in Virtual Reality*
2. Aim
A short paragraph describing the computer science problem that your project is
investigating.

You can describe the context of the problem but need to separate out the specifics of what
you will be studying.

This does not need to describe how you solve the problem or with what algorithms or tools,
unless that is fundamental to the work, e.g. your project is studying a particular algorithm or
technique.

Surgeons use 3D anatomical models e.g., the liver, to better familiarise themselves with the patient and their working environment before operating. This preparation reduces the operation's invasiveness and provides a quicker insight to the issue at hand. Typically, this model investigation and viewing is done on-screen using a joystick, offering limited inisght and difficult navigation. Futhermore, the tool also requires a steep learning curve before efficient use can be made of it.

A new method of interacting with these 3D models is needed. It must meet the rquirements of:
- easy and intuitive to use
- improved perception
- improved navigation of the model

To achieve this, the viewing space needs to be transformed. A virtual reality is the best way to view a 3D model from all perspectives. The next step concerns navigation: hand-gestures make the most sense as they complement the realistic experience and for this AI is needed to interpret these gestures. Ideally this new approach will enable system to simply hot-swap any model and render it into this virtual space. To render the model, the import will require complex mesh repairing, cleaning, simplification and other processing.

3. Objectives (up to 5)
Objectives should be SMART – Specific, Measurable, Achievable, Relevant, Time-bound.
Objectives should be a list of tasks that collectively meet the Aim of your project (makes
them Specific and Relevant)
Consider what you need to achieve to reach your Aim, as stages of your project.
Normal parts of the project such as literature review and report writing are not Objectives.

1. Develop a 3D model preprocessing pipeline that automatically repairs, simplifies, and optimizes anatomical meshes for real-time VR rendering while preserving critical topological features for surgical accuracy.

2. Implement a real-time hand-gesture recognition system using the Varjo XR-4/Magic Leap 2 APIs that accurately interprets complex 3D hand movements with precision for intuitive model manipulation.

3. Design and develop a gesture-to-action mapping framework that translates recognized hand movements into precise 3D navigation commands (rotation, zoom, pan, selection) with appropriate feedback and visual confirmation.

4. Conduct a comparative usability evaluation measuring task completion time, error rates, and user satisfaction between the hand-gesture interface and traditional joystick control with at least 10 participants from technical backgrounds.

5. Optimize the integrated system performance to achieve consistent high framerate rendering in VR while maintaining reasonable latency for gesture recognition to ensure a comfortable, user-friendly experience.

4. Deliverables (up to 5)
Deliverables are concrete items produced as part of your project. They are the evidence
required to show you have met your Objectives, and ultimately your Aim.
You should link them to your Objectives such that it is clear which Deliverable relates to
which objective (makes the Objective Measurable and Achievable).

Your final report and your software repository can both be considered Deliverables. You
may wish to further sub-divide this, for example if you project delivers several distinct
software items or particular chapters of your report are relevant.
This is the starting point for a plan, which you should also work on with your supervisor.

 1. Final report
 2. Software Repository
	 1. 3D mesh preprocessing toolkit with automated hole-filling, decimation, and optimization algorithms
	 2. Real-time hand gesture recognition module with trained models and calibration utilities
	 3. Unity-based VR integration framework with customizable gesture mappings
	 4. Performance benchmarking and testing suite
 3. Functional Prototype Application demonstrating complete workflow from model import to immersive hand-controlled navigation with support for multiple anatomical structures.
 4. Evaluation Dataset & Results including recorded user sessions, performance metrics, comparative analysis, and structured feedback from usability testing.

5. Plan
A schedule for your project from now until the final submission of the report (week 10 of
semester 2). Weekly is probably an appropriate level of planning for most people.
Use your Deliverables as milestones for your progress (makes the Objective Achievable and
Time-bound).

Allow time for completing evaluation of your work as well as completing development.
Allow time for writing up, and consider how you will write up – regularly and incrementally,
or later, once work is complete.

Please consider when there are other demands there are on your time, e.g. exams,
coursework, holidays.

#
# Semester 1
Week 06 (w/c 03/11)
- Project outline approval
- Literature review: VR interaction techniques & medical visualization
- Setup development environment (Unity, Varjo SDK/Magic Leap2 software)

Week 07 (w/c 10/11)
- Research 3D mesh processing algorithms
- Acquire and test sample anatomical models
- Begin mesh preprocessing implementation

Week 08 (w/c 17/11)
- Complete mesh preprocessing pipeline
- Test with complex liver models
- Start hand tracking API integration

Week 09 (w/c 24/11)
- Implement basic gesture recognition (grab, rotate, zoom)
- Integrate with simple 3D model in VR
- Milestone: Basic gesture control working

Week 10 (w/c 01/12)
- Refine gesture accuracy and sensitivity
- Add advanced gestures (pan, select, reset view)
- Begin writing Chapter 2 (Literature Review)

Week 11 (w/c 08/12)
- Complete core gesture mapping system
- Initial performance optimization
- Milestone: All planned gestures implemented
#
# Break
Week 12-13 (w/c 15/12 - 22/12)
- Holiday

Week 13- 15 (w/c 22/12 - 05/01)
- Light work: Continue literature review writing
- Plan evaluation methodology
- Prepare ethics considerations documentation

#
# Semester 2
Week 01 (w/c 12/01)
- System integration testing
- Fix compatibility issues between components
- Begin Chapter 3 (Methodology)

Week 02 (w/c 19/01)
- Develop evaluation protocol
- Create testing scenarios and tasks
- Prepare participant materials

Week 03 (w/c 26/01)
- Conduct pilot testing (3-5 participants)
- Refine system based on feedback
- Milestone: System ready for evaluation

Week 04 (w/c 02/02)
- Run formal user evaluation sessions
- Collect performance data and user feedback
- Begin data analysis

Week 05 (w/c 09/02)
- Complete all user testing
- Analyze comparative results
- Start Chapter 4 (Results)

Week 06 (w/c 16/02)
- Complete results analysis
- Draft Chapter 5 (Discussion)
- Milestone: Evaluation complete

Week 07 (w/c 23/02)
- Full draft completion (all chapters)
- Initial proofreading and formatting
- Prepare appendices

Week 08 (w/c 02/03)
- Supervisor feedback incorporation
- Technical refinement based on findings
- Final performance optimization

Week 09 (w/c 09/03)
- Final proofreading and formatting
- Reference checking
- Submission preparation

Week 10 (w/c 16/03)
- FINAL SUBMISSION
- Buffer week for unexpected delays

6. Risk
A brief discussion of how to mitigate risk in your project and ensure sufficient work will be
completed for final submission.
This could include prioritisation of Objectives and Deliverables or development of
prototypes as early-stage deliverables.
This could include some contingency in your plan for delays.

- Hand tracking accuracy issues: Some form of confidence scoring will be needed to assess accuracy
- Performance bottlenecks: Progressive mesh loading may severely impact the system; maintain joystick compatibility as backup
- VR motion sickness: Include comfort settings (snap turning, reduced movement); rigorous testing with multiple users early in development

7. Ethics
Describe the ethical issues associated with your project and how you will address them.
For example, proper handling of data sets, user testing, etc.
There is a lecture in Week 6 that you must attend and a further advice session in Week 7 if
you need guidance on how to properly consider ethics.
If you believe there are no ethical issues associated with your project you should state that
here.

- User Testing: All participants will provide informed consent; right to withdraw at any time; no medical professionals required for initial testing
- Health and Safety: VR usage guidelines provided; regular breaks enforced; participants screened for epilepsy or motion sickness susceptibility
- Intellectual Property: Clear acknowledgment of university and individual contributions; no use of proprietary medical data.
Ethical approval is required for the user-testing portion.