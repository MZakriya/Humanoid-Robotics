// @ts-check

/** @type {import('@docusaurus-plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: Embodied Intelligence',
      items: [
        'module1-embodied-intelligence',
        'module1-embodied-intelligence/1.1-introduction',
        'module1-embodied-intelligence/1.2-historical-foundations',
        'module1-embodied-intelligence/1.3-embodied-cognition',
        'module1-embodied-intelligence/1.4-perception-action-coupling',
        'module1-embodied-intelligence/1.5-sensorimotor-learning',
        'module1-embodied-intelligence/1.6-case-studies'
      ],
    },
    {
      type: 'category',
      label: 'Module 2: ROS 2 (Robot Operating System)',
      items: [
        'module2-ros2-fundamentals',
        'module2-ros2-fundamentals/2.1-architecture-concepts',
        'module2-ros2-fundamentals/2.2-nodes-and-topics',
        'module2-ros2-fundamentals/2.3-services-actions',
        'module2-ros2-fundamentals/2.4-package-management',
        'module2-ros2-fundamentals/2.5-best-practices',
        'module2-ros2-fundamentals/2.6-ros2-examples'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Kinematics',
      items: [
        'module3-kinematics',
        'module3-kinematics/3.1-forward-kinematics',
        'module3-kinematics/3.2-inverse-kinematics',
        'module3-kinematics/3.3-dh-convention',
        'module3-kinematics/3.4-jacobian-matrices',
        'module3-kinematics/3.5-kinematic-chains',
        'module3-kinematics/3.6-kinematic-applications'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: 3D Simulation (Gazebo-Unity)',
      items: [
        'module4-3d-simulation',
        'module4-3d-simulation/4.1-simulation-setup',
        'module4-3d-simulation/4.2-gazebo-integration',
        'module4-3d-simulation/4.3-unity-integration',
        'module4-3d-simulation/4.4-sensor-simulation',
        'module4-3d-simulation/4.5-sim2real-gap',
        'module4-3d-simulation/4.6-simulation-best-practices'
      ],
    },
    {
      type: 'category',
      label: 'Module 5: VSLAM',
      items: [
        'module5-vslam',
        'module5-vslam/5.1-feature-detection',
        'module5-vslam/5.2-camera-models',
        'module5-vslam/5.3-pose-estimation',
        'module5-vslam/5.4-loop-closure',
        'module5-vslam/5.5-vslam-algorithms',
        'module5-vslam/5.6-real-world-applications'
      ],
    },
    {
      type: 'category',
      label: 'Module 6: Motion Planning',
      items: [
        'module6-motion-planning',
        'module6-motion-planning/module6-motion-planning-6.1-path-planning-algorithms',
        'module6-motion-planning/module6-motion-planning-6.2-configuration-space',
        'module6-motion-planning/module6-motion-planning-6.3-sampling-based',
        'module6-motion-planning/module6-motion-planning-6.4-trajectory-optimization',
        'module6-motion-planning/module6-motion-planning-6.5-dynamic-motion',
        'module6-motion-planning/module6-motion-planning-6.6-multi-robot'
      ],
    },
    {
      type: 'category',
      label: 'Module 7: DRL with Isaac Sim',
      items: [
        'module7-drl-isaac-sim',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.1-reinforcement-learning',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.2-deep-q-networks',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.3-isaac-sim-setup',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.4-training-agents',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.5-transfer-learning',
        'module7-drl-isaac-sim/module7-drl-isaac-sim-7.6-advanced-techniques'
      ],
    },
    {
      type: 'category',
      label: 'Module 8: Manipulation & HRI',
      items: [
        'module8-manipulation-hri',
        'module8-manipulation-hri/module8-manipulation-hri-8.1-robot-manipulation',
        'module8-manipulation-hri/module8-manipulation-hri-8.2-grasping-strategies',
        'module8-manipulation-hri/module8-manipulation-hri-8.3-force-control',
        'module8-manipulation-hri/module8-manipulation-hri-8.4-human-robot-interaction',
        'module8-manipulation-hri/module8-manipulation-hri-8.5-safety-collaboration',
        'module8-manipulation-hri/module8-manipulation-hri-8.6-assistive-robotics'
      ],
    },
    {
      type: 'category',
      label: 'Module 9: VLA-Cognitive Robotics',
      items: [
        'module9-vla-cognitive-robotics',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.1-vision-language-action-models',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.2-cognitive-architectures',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.3-memory-learning',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.4-task-planning',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.5-natural-language',
        'module9-vla-cognitive-robotics/module9-vla-cognitive-robotics-9.6-ethical-considerations'
      ],
    },
    {
      type: 'category',
      label: 'Module 10: Capstone-Ethics',
      items: [
        'module10-capstone-ethics',
        'module10-capstone-ethics/module10-capstone-ethics-10.1-integration-all-modules',
        'module10-capstone-ethics/module10-capstone-ethics-10.2-complete-robot-system',
        'module10-capstone-ethics/module10-capstone-ethics-10.3-project-implementation',
        'module10-capstone-ethics/module10-capstone-ethics-10.4-ethical-implications',
        'module10-capstone-ethics/module10-capstone-ethics-10.5-societal-impact',
        'module10-capstone-ethics/module10-capstone-ethics-10.6-professional-responsibility'
      ],
    }
  ],
};

module.exports = sidebars;