// Add your constants here
export const API_VERSION = 'v1';
export const API_BASE_URL = 'http://localhost:8000/api';

export const LOG_LEVELS = {
  DEBUG: 'Debug',
  INFO: 'Info',
  WARNING: 'Warning',
  ERROR: 'Error',
} as const;

export const QUEUE_TYPES = {
  FIFO: 'FIFO',
  STANDARD: 'Standard',
} as const;

export const RUNTIME_INTERVALS = {
  '1MINUTE': '1 Minute',
  '3MINUTE': '3 Minutes',
  '5MINUTE': '5 Minutes',
  '15MINUTE': '15 Minutes',
} as const;

export const STRATEGIES = {
  '001': 'Strategy 001',
  '002': 'Strategy 002',
} as const;

export const REGIONS = {
  'ap-south-1': 'Asia Pacific (Mumbai)',
  'us-east-1': 'US East (N. Virginia)',
  'eu-west-1': 'EU (Ireland)',
} as const;

// Type definitions for the values
export type LogLevel = keyof typeof LOG_LEVELS;
export type QueueType = keyof typeof QUEUE_TYPES;
export type RuntimeInterval = keyof typeof RUNTIME_INTERVALS;
export type Strategy = keyof typeof STRATEGIES;
export type Region = keyof typeof REGIONS;

