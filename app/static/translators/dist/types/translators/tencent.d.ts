import { PronunciationSpeed, TranslationResult } from "../types";
/**
 * Tencent translator.
 */
declare class TencentTranslator {
    channel: any;
    /**
     * Max retry times.
     */
    MAX_RETRY: number;
    /**
     * Request tokens
     */
    qtk: string;
    qtv: string;
    /**
     * Base url.
     */
    BASE_URL: string;
    /**
     * Request headers.
     */
    HEADERS: {};
    /**
     * Language to translator language code.
     */
    LAN_TO_CODE: Map<string, string>;
    /**
     * Translator language code to language.
     */
    CODE_TO_LAN: Map<string, string>;
    /**
     * TTS audio instance.
     */
    AUDIO: HTMLAudioElement;
    constructor(channel: any);
    /**
     * Get supported languages of this API.
     *
     * @returns supported languages
     */
    supportedLanguages(): Set<string>;
    /**
     * Request Tencent translate home page in a new tab to update cookies.
     *
     * @returns request finished
     */
    requestHomePage(): Promise<void>;
    /**
     * Update request tokens.
     *
     * @returns request Promise.
     */
    updateTokens(): Promise<void>;
    /**
     * Parse Google translate result.
     *
     * @param response Google translate response
     * @param originalText original text
     *
     * @returns parsed result
     */
    parseResult(response: any, originalText: string): TranslationResult;
    /**
     * Detect language of given text.
     *
     * @param text text to detect
     *
     * @returns detected language Promise
     */
    detect(text: string): Promise<string | undefined>;
    /**
     * Translate given text.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns translation Promise
     */
    translate(text: string, from: string, to: string): Promise<TranslationResult>;
    /**
     * Pronounce given text.
     *
     * @param text text to pronounce
     * @param language language of text
     * @param speed "fast" or "slow"
     *
     * @returns pronounce finished
     */
    pronounce(text: string, language: string, _speed: PronunciationSpeed): Promise<void>;
    /**
     * Pause pronounce.
     */
    stopPronounce(): void;
}
export default TencentTranslator;
