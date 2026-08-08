// =========================================================================
// NEUTRAL BODY POSTURE (NBP) SEAT INSERT TEMPLATE
// This script models a non-functional visual mockup of an articulated 
// seat insert based on historical 128-degree microgravity posture metrics.
// For stationary display and geometric reference only.
// =========================================================================

// --- PARAMETERS ---
seat_width      = 24.0;   // Interior tray width constraint (inches)
pelvic_length   = 8.0;    // Lower seat base panel length (inches)
thigh_length    = 18.0;   // Forward thigh support panel length (inches)
thoracic_length = 24.0;   // Upper backrest panel length (inches)
tray_depth      = 3.0;    // Containment wall height (inches)
wall_thick      = 0.25;   // Sheet thickness for template (inches)

// NBP Geometry Angles
nbp_torso_angle = 128.0;  // Trunk-to-thigh angle profile
thigh_lift_angle = 15.0;  // Angle of thigh pan relative to floor

$fn = 50;

module base_panel(length, width, depth, wall) {
    difference() {
        cube([width, length, depth]);
        translate([wall, -1, wall])
            cube([width - (wall * 2), length + 2, depth]);
    }
}

module nbp_assembly() {
    union() {
        // 1. Pelvic / Lower Seat Base
        color("SlateGray")
            base_panel(pelvic_length, seat_width, tray_depth, wall_thick);
        
        // 2. Thigh Support Panel (Articulated forward at a lift angle)
        translate([0, pelvic_length, 0])
            rotate([-thigh_lift_angle, 0, 0])
                color("Charcoal")
                    base_panel(thigh_length, seat_width, tray_depth, wall_thick);
        
        // 3. Thoracic Upper Backrest Panel (Articulated at the 128-degree NBP offset)
        translate([0, 0, 0])
            rotate([180 - nbp_torso_angle, 0, 0])
                translate([0, -thoracic_length, 0])
                    color("Silver")
                        base_panel(thoracic_length, seat_width, tray_depth, wall_thick);
    }
}

// Render the parametric visual assembly
nbp_assembly();

