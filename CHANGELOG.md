# Changelog

## 1.8.14

- Stop retrying the Dreame login once the account rejects the stored
  password: the account locks after 5 failed logins. Home Assistant now asks
  to re-authenticate instead (*Reauthenticate* on the integration card). A
  revoked session falls back to a single login with the stored password, so
  the integration reconnects on its own when the password did not change.
- Fix the re-authentication flow: it crashed and never saved the new
  password. It now opens the account form, saves the new password and
  reloads the integration (#34).

## 1.8.13

- Cutting height control for the A1 Pro (#30, thanks @simonschaubel): a
  *Cutting Height* number entity (3.0 to 7.0 cm in 0.5 cm steps) and the
  `dreame_mower.mower_set_cutting_height` service, map-wide or for one zone
  (`segment_id`). Setting a zone height switches the map to per-zone
  preferences. The current preference record is always read before it is
  written, so the other mowing settings are kept. Heights are refreshed at
  most every 10 minutes, and not while the mower is asleep or unreachable.

## 1.8.12

- Current mowing zone: clear it when no zone is active (only pending or
  completed zones are reported) instead of reporting a completed zone, and
  ignore late zone events while the A1 Pro is docked, charging or returning
  to base (#21, thanks @piuskamil).

## 1.8.11

- Fix the integration options flow (*Configure*) crashing with a 500 error on
  recent Home Assistant versions: the options handler no longer assigns the
  read-only `config_entry` property. Requires Home Assistant 2024.11 or newer.
- Stop reporting normal A1 Pro task/dock status codes (53, 54, 70, 72) as
  errors. Code 54 is sent on every docking/charging and was surfaced as
  "Edge sensor error" with an `error_54` notification (#27).

## 1.8.10

- Keep the A1 Pro state, charging status, and battery sensors registered when
  the initial cloud property response is incomplete.
- Restore the current mowing zone from Dreame cloud storage after Home
  Assistant starts or reconnects during an active mowing task, including the
  zone name configured in the Dreame app/map.

## 1.8.9

- Fix A1 Pro zone mowing by using the native mower task API instead of the
  vacuum-derived `START_CUSTOM` segment payload.

## 1.8.8

- Limit maintained hardware support to the Dreame A1 Pro
  (`dreame.mower.g2422`).
- Keep map camera timestamps out of the entity state to reduce Activity and
  recorder noise. The live map and diagnostic update attributes remain
  available.
- Add current mowing zone ID and state sensors for the A1 Pro.
- Add a dynamic charging-aware battery icon.
- Replace vacuum-oriented cleaning labels with mower terminology in English
  and French.
- Fix the recent-change polling condition so the faster interval is only used
  during the intended 60-second window.
- Add A1 Pro-specific issue forms and contribution guidance.

This release intentionally contains no A2, A3, or MOVA-specific changes.
