# AutoRescue Professional Workflow

## Purpose

AutoRescue is a role-based roadside assistance workflow for drivers, mechanics, and operators. The product goal is to move a roadside case from intake to mechanic dispatch with clear ownership, location context, and status visibility.

## Roles

| Role | Primary screen | Responsibility |
| --- | --- | --- |
| Driver | Customer dashboard, request form | Create requests with vehicle, issue, and pickup location |
| Mechanic | Mechanic dashboard, available queue | Review pending work, judge distance/context, accept suitable requests |
| Admin | Command center | Monitor demand, supply, user growth, and request throughput |

## Request Lifecycle

1. Intake
   - Driver opens `Request roadside help`.
   - Driver selects vehicle type, describes the issue, and pins the pickup point.
   - The system validates vehicle, issue length, latitude, and longitude.

2. Queue
   - New requests enter the platform with `Pending` status.
   - Customer dashboard shows the request in the driver's recent activity.
   - Mechanic dashboard and available requests page show the request to mechanics.

3. Triage
   - Request priority is inferred from issue keywords and request age.
   - Urgent language such as brake, engine, smoke, flat, battery, no-start, or overheat receives high priority.
   - Mechanics see distance labels when their saved location is available.

4. Dispatch
   - A mechanic reviews customer context, distance, age, and issue detail.
   - Mechanic accepts the request.
   - The system changes status from `Pending` to `Accepted`.

5. Operations Review
   - Admin dashboard tracks users, mechanics, open demand, and completed work.
   - Request history gives every role a clear view of current and past cases.

## Professional Demo Flow

1. Run `.\.venv\Scripts\python.exe init_db.py`.
2. Start the app with `.\.venv\Scripts\python.exe app.py`.
3. Log in as `customer@example.com` with `password123`.
4. Create a roadside request from the customer dashboard.
5. Log out, then log in as `mechanic@example.com` with `password123`.
6. Open the live queue and accept the new request.
7. Log in as `admin@example.com` with `admin123`.
8. Review the command center metrics and recent request table.

## Quality Checklist

- Request form blocks empty vehicle and issue values.
- Issue description must be meaningful enough for dispatch.
- Location fields are always populated before submit.
- Mechanic-only routes reject customer and admin users.
- Customer users only see their own request history.
- Admin dashboard does not expose mutation actions by accident.
- Fetch requests return JSON-safe errors.
- Browser page errors render user-friendly error screens.

## Visual Workflow Principles

- Keep primary actions obvious: request help, browse queue, accept job, view history.
- Use status chips for quick scanning instead of long labels.
- Keep role dashboards dense but readable: metrics first, workflow next, records last.
- Use warm highlight colors for urgency and teal/green for confirmation.
- Avoid decorative UI that competes with operational content.

## Future Enhancements

- Add mechanic assignment history to each request.
- Add completed status transition after service resolution.
- Add admin filters for open, accepted, and completed work.
- Add estimated arrival time once mechanic routing is available.
- Add audit timestamps for accepted and completed transitions.
