export interface VerificationResult {
    phone_valid: boolean;
    email_valid: boolean;
    risk_score: number;
    risk_factors?: string[];
    phone_details?: string;
    email_details?: string;
}

export interface Verification {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    status: 'valid' | 'invalid' | 'risky';
    risk_score: number;
    timestamp: string;
    details: VerificationResult;
}

export interface HistoryResponse {
    verifications: Verification[];
    total: number;
}

export interface VerificationFormData {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
} 