# IntelliTrader Development Rules

[Previous rules content...]

### API and Error Handling Guidelines

#### Backend (FastAPI)

1. **Response Format**:

   ```python
   {
       "message": str,  # User-friendly message
       "data": Any     # Response payload
   }
   ```

   OR for errors:

   ```python
   {
       "error": {
           "message": str,        # User-friendly error message
           "data": Optional[Any], # Additional error context
           "request_id": str,     # Unique request identifier
           "path": str,          # Request path
           "method": str         # HTTP method
       }
   }
   ```

2. **Error Handling Layers**:

   - **Global Middleware**: Handles all exceptions, adds request context
   - **Service Layer**: Throws domain-specific ApiExceptions
   - **Repository Layer**: Returns success/error results

3. **Exception Types**:
   - Use `ApiException` class with specific factory methods:
     - `validation_error`: For invalid input data
     - `not_found`: For missing resources
     - `internal_server_error`: For system errors
     - `database_error`: For database operation failures

#### Frontend (Next.js)

1. **API Client Structure**:

   - Centralized in `lib/http/fetch.ts`
   - Type-safe methods: get<T>, post<T>, patch<T>, delete<T>
   - Consistent error handling with ApiError class

2. **Type Definitions**:

   ```typescript
   interface ApiSuccessResponse<T> {
     message: string;
     data: T;
   }

   interface ApiErrorResponse {
     error: {
       message: string;
       data?: any;
       request_id: string;
       path: string;
       method: string;
     };
   }
   ```

3. **Error Handling Flow**:

   - Network errors → User-friendly messages
   - API errors → Structured error responses
   - Validation errors → Field-specific feedback

4. **Toast Notifications**:
   - Success: Green toast with action buttons
   - Error: Red toast with retry option
   - Loading: Progress indicator
   - Use sonner for consistent styling

#### Usage Example

1. **Backend Service**:

   ```python
   async def save_preferences(self) -> Dict[str, Any]:
       try:
           # Validate input
           preferences_schema = PreferencesSchema(**self.request_parameters)
       except ValueError as e:
           raise ApiException.validation_error(
               message="Invalid preferences data",
               data={"fields": str(e)}
           )

       # Process and return
       return {
           "message": "Success message",
           "data": result_data
       }
   ```

2. **Frontend Component**:
   ```typescript
   async function handleSave(data: PreferencesSchema) {
     const loadingToast = showLoadingToast("Saving...");
     try {
       const result = await api.post<PreferencesSchema>(
         "/settings/preferences",
         data
       );
       showSuccessToast("Saved successfully");
       return result;
     } catch (error) {
       showErrorToast(error as Error | ApiError);
       throw error;
     } finally {
       dismissToast(loadingToast);
     }
   }
   ```

### Best Practices

1. **Error Messages**:

   - User-facing: Clear, actionable, non-technical
   - Logs: Detailed, with context for debugging
   - Include request IDs for traceability

2. **Status Codes and Error Types**:

   - All available API exceptions and their status codes
     {
     validation_error: 400, // Invalid input data
     unauthorized_error: 401, // Authentication required
     forbidden_error: 403, // Insufficient permissions
     not_found: 404, // Resource doesn't exist
     method_not_allowed: 405, // HTTP method not supported
     conflict_error: 409, // Resource conflict
     precondition_failed: 412, // Precondition check failed
     rate_limit_exceeded: 429, // Too many requests
     internal_server_error: 500, // Unexpected server error
     database_error: 500, // Database operation failed
     not_implemented: 501, // Feature not implemented
     bad_gateway: 502, // Invalid response from upstream
     service_unavailable: 503, // Service temporarily down
     gateway_timeout: 504 // Upstream timeout
     }

3. **Performance**:

   - Add request timeouts
   - Implement retries for network errors
   - Cache responses where appropriate

4. **Security**:
   - Sanitize error messages
   - Don't expose internal details
   - Log sensitive data appropriately
