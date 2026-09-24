# EATM Notices

## Purpose

This document defines how the EATM Student Assistant should handle college notices.

EATM maintains an official Notice Board on its website where academic, examination, student-activity, administrative, and other institutional notices may be published.

Official Notice Board:

https://www.eatm.in/notice-board/

## Notice Categories

EATM notices may contain information about:

* Academic schedules
* Examination dates
* Class tests
* Admission-related activities
* Registration
* Fee-related instructions
* Training and placement activities
* Student activities
* Workshops and seminars
* Hostel-related instructions
* Library-related information
* Administrative instructions
* Events and programmes
* Scholarships and student welfare
* Department-specific activities

## Current Notices

Notices are time-sensitive.

A notice containing a date, deadline, examination schedule, class schedule, fee requirement, event, or other temporary instruction must not automatically be treated as current.

The assistant should check the notice date and context before presenting information to a student.

## Historical Notices

The official EATM Notice Board contains older notices as well as newer institutional information. For example, the website currently displays notices from the 2023-24 academic period alongside other information.

Historical notices may be useful for understanding previous procedures, but they must not be presented as current instructions.

## Current Examination Notices

If a student asks:

* "When is my exam?"
* "What is the latest exam notice?"
* "When is the next class test?"
* "When do I collect my admit card?"

the assistant must use a current verified examination notice if one is available in the knowledge base.

If no current notice is available, the assistant must tell the student that a current verified notice is not available.

The assistant must never guess examination dates.

## Current Placement Notices

If a student asks:

* "Which company is coming?"
* "When is the placement drive?"
* "Who is eligible?"
* "What is the interview date?"

the assistant must use a current verified placement notice if one has been added to the knowledge base.

It must not infer current recruitment information from historical notices.

## Current Admission Notices

Admission deadlines, counselling dates, registration dates, document requirements, and fee-payment deadlines are time-sensitive.

The assistant must not provide these details from an old notice as if they are current.

Students should verify the latest official admission notice when current information is not available.

## Notice Source Metadata

When notices are added to the knowledge base, each notice should ideally contain:

* Notice title
* Notice date
* Category
* Source URL
* Publication year
* Relevant deadline or event date
* Notice content

This metadata helps the retrieval system distinguish current information from historical information.

## Notice Update Procedure

When a new official notice is added:

1. Save the notice in the appropriate knowledge-base category.
2. Include the official source URL.
3. Include the notice date.
4. Preserve the original meaning of the notice.
5. Run the knowledge-base ingestion process again.
6. Test retrieval using questions related to the notice.

Old notices should not be deleted automatically because they may be useful for historical reference.

## Unavailable Information

If a student asks about a current notice that is not present in the knowledge base, the assistant should respond that the current information is not available in its knowledge base and direct the student to the official EATM Notice Board.

It must not fabricate a notice.

## Official Sources

EATM Notice Board:

https://www.eatm.in/notice-board/

EATM official website:

https://www.eatm.in/

## Assistant Grounding Rule

The assistant must distinguish between:

1. Current verified notices.
2. Historical notices.
3. General institutional information.
4. Information that is not available.

A historical notice must never be presented as a current announcement.

When the date or validity of a notice cannot be established, the assistant should clearly state the uncertainty and direct the student to the official EATM Notice Board.
