# Project Context: StrumSphere /FrancoUke

## 🌐 Overview

This Django project serves two music-focused sites, **FrancoUke** and **StrumSphere**, with shared backend logic. Users can view, create, update, and manage ukulele chord charts, including metadata and chord formatting.

---

## 🧩 Core App Structure

### `Song` Model (`models.py`)
- Stores user-contributed chord charts in **ChordPro** format.
- Fields include:
  - `songTitle`, `songChordPro`, `lyrics_with_chords` (auto-generated JSON),
  - Metadata fields parsed from ChordPro: `title`, `artist`, `capo`, `key`, etc.
  - `site_name`: distinguishes content between **FrancoUke** and **StrumSphere**.
- ChordPro content is processed and converted to JSON for rendering and PDF generation.

---

## 🔗 URL Routing (`urls.py`)
Routes are duplicated for both FrancoUke and StrumSphere using site-specific prefixes:

- **Song Management**:
  - `/<site>/song/<id>/`: View song details.
  - `/<site>/song/new/`, `update/`, `delete/`: Create/update/delete functionality.
- **Artists**:
  - Filter by artist name or initial letter.
- **PDF Exports**:
  - Single and multi-song PDF generation (`preview_pdf`, `generate_single_song_pdf`, etc.).
- **Chord Dictionary**:
  - Site-specific dictionary views under `/FrancoUke/` or `/StrumSphere/`.

---

## 🧠 Views (`views.py`)
Implements a mix of CBVs and FBVs:
- Uses `ScoreView`, `SongCreateView`, `SongUpdateView`, and `SongDeleteView`.
- Custom functions handle PDF creation and formatting (`generate_single_song_pdf`, etc.).
- Views respect the `site_name` context to distinguish content and routing.

---

## 🛠 Notable Features
- **Multi-site Logic**: Single codebase powers two branded experiences.
- **Dynamic Metadata Extraction**: Parses ChordPro content for structured metadata.
- **User-Contributed Content**: Integrated with Django’s `User` model.
- **Tagging**: Via `TaggableManager` for song classification.
