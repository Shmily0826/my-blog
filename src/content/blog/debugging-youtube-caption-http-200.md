---
title: 'Debugging a YouTube Caption Failure That Still Returned HTTP 200'
description: 'An EchoLearn investigation into a YouTube Player response that returned HTTP 200 but exposed no caption tracks, using controlled transport comparisons and a positive control.'
pubDate: '2026-09-03'
lang: 'en'
draft: true
---


A request can succeed at the network layer and still fail completely for the user.

I ran into this while investigating YouTube caption reliability in EchoLearn, an English-learning project that turns video content into sentence-level study material, vocabulary practice, and optional AI-assisted analysis.

For the video-based learning flow, a usable transcript is an upstream dependency:

`video URL → captions → sentences → vocabulary / analysis → review`

One failure case looked healthy at first. The YouTube Player request returned:

`HTTP 200`

But the response also reported:

`LOGIN_REQUIRED`

and exposed:

`0 caption tracks`

So the transport had succeeded, but EchoLearn still had nothing it could turn into study material.

That distinction became the most useful part of the investigation.

## The failure looked healthy from the outside

An HTTP status code answers a narrow question: did the server return a response?

It does not answer whether the response contains the application data I need.

For the failing target video, the Player endpoint returned HTTP 200 while exposing no caption tracks.

A known-good positive control behaved differently in the same environment:

`HTTP 200 → OK → 6 caption tracks → English track → timedtext 200 → 61 usable lines`

This was useful because it showed that the test environment was not simply broken.

The server could reach YouTube. The Player request could expose captions. The timed-text request could return a usable transcript.

The failure was specific enough to investigate further.

## A plausible hypothesis: the HTTP client fingerprint

One possible explanation was the transport itself.

The requests were running from a VPS rather than a normal consumer browser. I had also been reading upstream documentation and issue reports about YouTube extraction failures, client impersonation, and request context.

That made a transport-level hypothesis reasonable:

> Maybe the target fails because the server-side HTTP/TLS fingerprint does not look enough like browser traffic.

Instead of changing several parts of the acquisition pipeline at once, I set up a narrower experiment.

The Player and timed-text request semantics were kept fixed while the HTTP transport changed.

I compared three variants:

- native Python HTTP
- `curl_cffi` with Chrome impersonation
- `curl_cffi` with Safari impersonation

These were transport impersonation tests, not full Chrome or Safari browser sessions.

I ran every variant against both the failing target and the same known-good positive control.

| Transport | Target video | Positive control |
| --- | --- | --- |
| Native Python | HTTP 200, `LOGIN_REQUIRED`, 0 tracks | HTTP 200, `OK`, 6 tracks, timedtext 200, 61 lines |
| `curl_cffi` Chrome | HTTP 200, `LOGIN_REQUIRED`, 0 tracks | HTTP 200, `OK`, 6 tracks, timedtext 200, 61 lines |
| `curl_cffi` Safari | HTTP 200, `LOGIN_REQUIRED`, 0 tracks | HTTP 200, `OK`, 6 tracks, timedtext 200, 61 lines |

Because the target exposed no tracks, there was no target timed-text request to make.

The important part was that the result did not move.

Changing the transport did not change the target Player state.

At the same time, the positive control remained healthy across all three variants.

## A negative result can still be useful

The experiment did not solve the caption problem.

It did remove one attractive direction from the top of the list.

If a simple raw HTTP/TLS fingerprint mismatch were the primary cause of this specific failure, I would expect Chrome or Safari transport impersonation to produce some meaningful change.

Instead, all three target requests converged on the same result:

`HTTP 200 → LOGIN_REQUIRED → 0 tracks`

Meanwhile, all three positive-control requests still reached 61 usable lines.

That substantially weakened the transport-fingerprint hypothesis for this case.

It does not prove that fingerprinting is irrelevant to YouTube generally. There are many other differences in request, session, network, and platform context that this experiment did not isolate.

But it was enough to stop treating the HTTP library itself as the most likely explanation.

That is useful progress.

Without a controlled experiment, it would have been easy to keep changing headers, libraries, proxy settings, or client profiles simply because each one sounded plausible.

## HTTP 200 is not application success

The larger lesson was about how success should be defined.

For a caption pipeline, this:

`response.status === 200`

is much too early to declare success.

There are several meaningful stages between a successful HTTP response and something a learner can actually use:

`Player response`

→ `playability state`

→ `caption tracks exposed`

→ `language / track selected`

→ `timed-text response`

→ `usable transcript lines`

The failing target made this obvious.

Its request was technically successful at the transport layer, but application-level acquisition had failed before a caption track was even available.

EchoLearn already performs semantic checks above HTTP status in its transcript paths. A response is not treated as a useful transcript simply because a request completed; usable transcript data must actually contain content. The code also distinguishes several typed failure outcomes rather than reducing every failure to one generic error.

The investigation suggests that this distinction should go further over time.

Player state, exposed track count, selected language, timed-text status, and usable-line count are all valuable diagnostic signals.

That does not mean every internal phase needs to become a user-facing error message. It means the system should preserve enough information to understand where acquisition stopped.

## Why the positive control mattered

The positive control was one of the simplest parts of the test, but also one of the most valuable.

Suppose I had only tested the failing video.

I would have seen:

`LOGIN_REQUIRED`

under native Python, Chrome impersonation, and Safari impersonation.

But I would not know whether:

- all three transports were incorrectly configured,
- the VPS could no longer retrieve any captions,
- the timed-text path was generally broken,
- or the failure was specific to the target.

The positive control removed much of that ambiguity.

It demonstrated that the same experiment could still reach:

`OK → 6 tracks → timedtext 200 → 61 usable lines`

That made the negative target result interpretable.

I now see positive controls as important for this kind of integration testing, especially when the external platform can return different behavior across videos and request contexts.

A single failure tells you that something failed.

A failure beside a healthy control tells you much more about where to look next.

## Changing how I investigate third-party failures

There was another process lesson in this work.

At first, it is tempting to reason almost entirely from your own codebase:

Which function is wrong?

Which header is missing?

Which provider should be retried?

But YouTube caption extraction is not a problem unique to EchoLearn. Mature open-source projects, upstream documentation, issue trackers, and recent reports contain useful evidence about how the platform behaves.

I started using those sources earlier to generate hypotheses.

The important distinction is that external evidence is not the conclusion.

The workflow I want is:

`external evidence → hypothesis → controlled experiment → local evidence`

For example, upstream discussion made browser-style transport impersonation worth testing.

The EchoLearn experiment then showed that this hypothesis did not explain the target failure by itself.

That prevented a plausible community explanation from turning into an assumed root cause.

It also gives me a better rule for AI-assisted engineering work: suggestions from tools, documentation, GitHub issues, or AI are inputs to an investigation. They still need to survive testing against the real system.

## Experimental work is not the same as shipped work

This distinction matters for another reason.

During a reliability investigation, I often build small harnesses, adapters, or diagnostic paths to answer one question.

Those experiments are useful evidence, but they are not automatically production features.

The native/Chrome/Safari transport matrix in this article came from an investigation harness. It should not be interpreted as “EchoLearn now runs three browser-impersonated caption clients in production.”

Likewise, a locally tested provider adapter or recovery idea is not something I should describe as deployed until it has actually passed the relevant validation and deployment process.

Keeping those boundaries explicit makes technical notes more trustworthy.

It also avoids a common failure mode in AI-assisted development: implementation can move quickly enough that a prototype, test harness, candidate, and production path start sounding like the same thing.

They are not.

## What remains unresolved

The target still returned `LOGIN_REQUIRED` and exposed zero caption tracks in this experiment.

The transport comparison narrowed the search space, but it did not determine the final cause of that Player state.

So this is not a “how I fixed YouTube captions” post.

The accurate conclusion is narrower:

> In this VPS experiment, changing native Python transport to Chrome- or Safari-impersonated `curl_cffi` did not change the target Player result, while the positive control stayed healthy. That substantially weakened a simple raw HTTP/TLS fingerprint explanation for this specific failure.

There are still variables above the raw transport layer to investigate.

That is where the next experiment needs to start.

## What I took away from the investigation

A few practices became much clearer from this debugging session.

First, define success at the application layer, not at the first successful network response.

Second, use a positive control when debugging an external integration. It turns many ambiguous failures into useful comparisons.

Third, change one variable at a time when possible. A failed hypothesis is still valuable when the experiment is controlled enough to interpret it.

Fourth, use upstream documentation, issue reports, open-source projects, and AI to generate hypotheses—but make the system itself provide the evidence.

And finally, keep investigation code, candidate implementations, and production behavior separate when describing what has actually been built.

The caption reliability problem is not fully solved yet.

But one explanation is now much less likely, the failure boundary is clearer, and the next investigation can begin from evidence instead of another guess.
