import type { AxiosRequestConfig } from "axios";
import { PronunciationSpeed, TranslationResult } from "../types";
/**
 * Bing translator interface.
 */
declare class BingTranslator {
    /**
     * Basic request parameters.
     */
    IG: string;
    IID: string | null;
    token: string;
    key: string;
    /**
     * Whether we have initiated tokens.
     */
    tokensInitiated: boolean;
    /**
     * TTS auth info.
     */
    TTS_AUTH: {
        region: string;
        token: string;
    };
    /**
     * Request count.
     */
    count: number;
    HTMLParser: DOMParser;
    /**
     * Max retry times.
     */
    MAX_RETRY: number;
    /**
     * Translate API host.
     */
    HOST: string;
    /**
     * Translate API home page.
     */
    HOME_PAGE: string;
    /**
     * Request headers.
     */
    HEADERS: {
        accept: string;
        "accept-language": string;
        "content-type": string;
    };
    /**
     * Language to translator language code.
     */
    LAN_TO_CODE: Map<string, string>;
    /**
     * Translator language code to language.
     */
    CODE_TO_LAN: Map<string, string>;
    /**
     * Audio instance.
     */
    AUDIO: HTMLAudioElement;
    /**
     * Get IG and IID for urls.
     *
     * @returns IG and IID Promise
     */
    updateTokens(): Promise<void>;
    /**
     * Parse translate interface result.
     *
     * @param result translate result
     * @param extras extra data
     *
     * @returns Parsed result
     */
    parseTranslateResult(result: any, extras: TranslationResult): TranslationResult;
    /**
     * Parse the lookup interface result.
     *
     * @param result lookup result
     * @param extras extra data
     *
     * @returns Parsed result
     */
    parseLookupResult(result: any, extras: TranslationResult): TranslationResult;
    /**
     * Parse example response.
     *
     * @param result example response
     * @param extras extra data
     *
     * @returns parse result
     */
    parseExampleResult(result: any, extras: TranslationResult): TranslationResult;
    /**
     * Get TTS auth token.
     *
     * @returns request finished Promise
     */
    updateTTSAuth(): Promise<void>;
    /**
     * Generate TTS request data.
     *
     * @param text text to pronounce
     * @param language language of text
     * @param speed pronouncing speed, "fast" or "slow"
     *
     * @returns TTS request data
     */
    generateTTSData(text: string, language: string, speed: PronunciationSpeed): string;
    /**
     * Transform binary data into Base64 encoding.
     *
     * @param buffer array buffer with audio data
     *
     * @returns Base64 form of binary data in buffer
     */
    arrayBufferToBase64(buffer: Iterable<number>): string;
    /**
     * Construct detect request parameters dynamically.
     *
     * @param text text to detect
     *
     * @returns constructed parameters
     */
    constructDetectParams(text: string): AxiosRequestConfig;
    /**
     * Construct translate request parameters dynamically.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns constructed parameters
     */
    constructTranslateParams(text: string, from: string, to: string): AxiosRequestConfig;
    /**
     * Construct lookup request parameters dynamically.
     *
     * @param text text to lookup
     * @param from source language
     * @param to target language
     *
     * @returns constructed parameters
     */
    constructLookupParams(text: string, from: string, to: string): AxiosRequestConfig;
    /**
     * Construct example request parameters dynamically.
     *
     * @param from source language
     * @param to target language
     * @param text original text
     * @param translation text translation
     *
     * @returns constructed parameters
     */
    constructExampleParams(from: string, to: string, text: string, translation: string): AxiosRequestConfig;
    /**
     * Construct TTS request parameters dynamically.
     *
     * @param text text to pronounce
     * @param lang language of text
     * @param speed pronounce speed
     *
     * @returns constructed parameters
     */
    constructTTSParams(text: string, lang: string, speed: PronunciationSpeed): AxiosRequestConfig<any>;
    /**
     * Request APIs.
     *
     * This is a wrapper of axios with retrying and error handling supported.
     *
     * @param constructParams request parameters constructor
     * @param constructParamsArgs request parameters constructor arguments
     * @param retry whether retry is needed
     *
     * @returns Promise of response data
     */
    request(constructParams: (...args: any[]) => AxiosRequestConfig, constructParamsArgs: string[], retry?: boolean): Promise<any>;
    /**
     * Get supported languages of this API.
     *
     * @returns {Set<String>} supported languages
     */
    supportedLanguages(): Set<string>;
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
     * This method will request the translate API firstly with 2 purposes:
     *     1. detect the language of the translating text
     *     2. get a basic translation of the text incase lookup is not available
     *
     * After that, it will attempt to request the lookup API to get detailed translation.
     * If that failed, the method will use the translation from the translate API instead.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns {Promise<Object>} translation Promise
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
    pronounce(text: string, language: string, speed: PronunciationSpeed): Promise<void>;
    /**
     * Pause pronounce.
     */
    stopPronounce(): void;
}
export default BingTranslator;
