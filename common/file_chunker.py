#!/usr/bin/env python3
import io
import sys
import math
import os
from pathlib import Path

CHUNK_SIZE = 45 * 1024 * 1024  # 45MB, under GitHub's 50MB limit

def get_chunk_name(name, idx, num_chunks):
  return f"{name}.chunk{idx+1:02d}of{num_chunks:02d}"

def get_manifest_path(name):
  return f"{name}.chunkmanifest"

def _chunk_paths(path, num_chunks):
  return [get_manifest_path(path)] + [get_chunk_name(path, i, num_chunks) for i in range(num_chunks)]

def get_chunk_targets(path, file_size):
  num_chunks = math.ceil(file_size / CHUNK_SIZE)
  return _chunk_paths(path, num_chunks)

def chunk_file(path, targets):
  manifest_path, *chunk_paths = targets
  with open(path, 'rb') as f:
    data = f.read()
  actual_num_chunks = max(1, math.ceil(len(data) / CHUNK_SIZE))
  assert len(chunk_paths) >= actual_num_chunks, f"Allowed {len(chunk_paths)} chunks but needs at least {actual_num_chunks}, for path {path}"
  for i, chunk_path in enumerate(chunk_paths):
    with open(chunk_path, 'wb') as f:
      f.write(data[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE])
  Path(manifest_path).write_text(str(len(chunk_paths)))
  os.remove(path)

def get_existing_chunks(path):
  if os.path.isfile(path):
    return [path]
  if os.path.isfile(manifest := get_manifest_path(path)):
    num_chunks = int(Path(manifest).read_text().strip())
    return _chunk_paths(path, num_chunks)
  raise FileNotFoundError(path)

def read_file_chunked(path):
  manifest_path = get_manifest_path(path)
  if os.path.isfile(manifest_path):
    num_chunks = int(Path(manifest_path).read_text().strip())
    return b''.join(Path(get_chunk_name(path, i, num_chunks)).read_bytes() for i in range(num_chunks))
  if os.path.isfile(path):
    return Path(path).read_bytes()
  raise FileNotFoundError(path)

class _ChunkedFile(io.RawIOBase):
  """Read-only file-like view that transparently assembles chunk files."""

  def __init__(self, chunk_blobs: list[bytes]):
    super().__init__()
    self._chunks = chunk_blobs
    self._idx = 0
    self._offset = 0

  def readable(self):
    return True

  def readinto(self, b):
    if self._idx >= len(self._chunks):
      return 0
    chunk = self._chunks[self._idx]
    remaining = len(chunk) - self._offset
    n = min(len(b), remaining)
    b[:n] = chunk[self._offset:self._offset + n]
    self._offset += n
    if self._offset >= len(chunk):
      self._idx += 1
      self._offset = 0
    return n


def open_file_chunked(path):
  """Open a file that may be stored as chunks, returning a buffered file-like object.

  If a chunk manifest exists for *path*, the chunks are assembled into a
  single contiguous read stream.  Otherwise the plain file is opened directly.
  """
  manifest_path = get_manifest_path(path)
  if os.path.isfile(manifest_path):
    num_chunks = int(Path(manifest_path).read_text().strip())
    chunks = [Path(get_chunk_name(path, i, num_chunks)).read_bytes() for i in range(num_chunks)]
    return io.BufferedReader(_ChunkedFile(chunks))
  if os.path.isfile(path):
    return open(path, 'rb')
  raise FileNotFoundError(path)



if __name__ == "__main__":
  path = sys.argv[1]
  chunk_paths = get_chunk_targets(path, os.path.getsize(path))
  chunk_file(path, chunk_paths)
