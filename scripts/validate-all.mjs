// Validate all schemas, manifests, and configs across the platform.
import fs from 'fs';
import path from 'path';

let failures = 0;
function check(desc, fn) {
  try { fn(); console.log('PASS:', desc); }
  catch (e) { failures++; console.log('FAIL:', desc, '-', e.message); }
}

// Validate all JSON schema files parse
const schemaDirs = ['quantum/schemas', 'cerebral-matrix/schemas', 'unicorn-tech/schemas'];
for (const dir of schemaDirs) {
  if (!fs.existsSync(dir)) continue;
  for (const f of fs.readdirSync(dir)) {
    if (f.endsWith('.json')) {
      check(`schema ${dir}/${f}`, () => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
    }
  }
}

// Validate root package.json
check('root package.json', () => JSON.parse(fs.readFileSync('package.json', 'utf8')));

console.log(failures === 0 ? '\nAll validations passed.' : `\n${failures} validation(s) failed.`);
process.exit(failures === 0 ? 0 : 1);
