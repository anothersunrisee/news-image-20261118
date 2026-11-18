// news-image-20261118 entry (Node 22, standard library only).
// The image is entry.png beside this file: a flat-vector front page
// summing up the world news of Wednesday 18 November 2026
// (Shenzhen summit, Gulf strikes, Kerch Bridge, Democrats 56-44,
// Voyager 1 one light-day). The program copies it to the output dir.
//
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// The program runs twice and both runs must write the same bytes,
// so this is a plain copy: no timestamps, no randomness, no network.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
copyFileSync(source, join(outDir, 'entry.png'));
