// API Response Types
export interface ApiSuccessResponse<T = any> {
  message: string;
  data: T;
}

export interface ApiErrorResponse {
  error: {
    message: string;
    data?: any;
    request_id: string;
    path: string;
    method: string;
  };
}

// Custom error class for API errors
export class ApiError extends Error {
  constructor(
    message: string,
    public readonly request_id: string,
    public readonly path: string,
    public readonly method: string,
    public readonly data?: any,
    public readonly status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }

  // Helper method to check if error is retryable
  public isRetryable(): boolean {
    return this.status ? this.status >= 500 || this.status === 429 : false;
  }

  // Helper method to get user-friendly error message
  public getUserMessage(): string {
    if (this.data?.fields) {
      return `Invalid input: ${this.data.fields}`;
    }
    return this.message || "An unexpected error occurred";
  }

  // Helper method to get technical error details for logging
  public getTechnicalDetails(): string {
    return `[${this.request_id}] ${this.method} ${this.path} - ${this.message}`;
  }
}

// Type guard to check if response is an error
export function isApiErrorResponse(
  response: any,
): response is ApiErrorResponse {
  return response && "error" in response;
}

// Type guard to check if response is successful
export function isApiSuccessResponse<T>(
  response: any,
): response is ApiSuccessResponse<T> {
  return response && "message" in response && "data" in response;
}

// Preferences Types
export interface Preferences {
  id?: number;
  user_id?: string;
  
  // General Settings
  debugger_mode: boolean;
  log_level: string;
  reset_app: boolean;
  prettier_print: boolean;
  
  // Trade Settings
  live_trade: boolean;
  topic_type: string;
  queue_type: string;
  strategy: string;
  historical_data_subscription: boolean;
  global_trade: boolean;
  runtime_interval: string;
  
  // Notification Settings
  notify_trades: boolean;
  notify_trades_email: boolean;
  notify_trades_push: boolean;
  notify_price_alerts: boolean;
  notify_price_alerts_email: boolean;
  notify_price_alerts_push: boolean;
  notify_portfolio: boolean;
  notify_portfolio_email: boolean;
  notify_portfolio_push: boolean;
  
  // System Settings
  secret_name: string;
  region_name: string;
  
  // Audit Fields
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  updated_by?: string;
  is_active: boolean;
}

export interface PreferencesResponse extends ApiSuccessResponse<Preferences> {}
