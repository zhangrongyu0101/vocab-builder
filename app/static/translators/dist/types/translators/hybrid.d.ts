import { PronunciationSpeed, TranslationResult } from "../types";
import BaiduTranslator from "./baidu";
import BingTranslator from "./bing";
import DeepLTranslator from "./deepl";
import GoogleTranslator from "./google";
import TencentTranslator from "./tencent";
export type HybridSupportedTranslators = "BaiduTranslate" | "BingTranslate" | "DeepLTranslate" | "GoogleTranslate" | "TencentTranslate";
export type HybridConfig = {
    selections: Selections;
    translators: HybridSupportedTranslators[];
};
export type Selections = Record<keyof TranslationResult, HybridSupportedTranslators>;
declare class HybridTranslator {
    channel: any;
    /**
     * Hybrid translator config.
     */
    CONFIG: HybridConfig;
    REAL_TRANSLATORS: {
        BaiduTranslate: BaiduTranslator;
        BingTranslate: BingTranslator;
        GoogleTranslate: GoogleTranslator;
        TencentTranslate: TencentTranslator;
        DeepLTranslate: DeepLTranslator;
    };
    MAIN_TRANSLATOR: HybridSupportedTranslators;
    constructor(config: HybridConfig, channel: any);
    /**
     * Update config.
     *
     * @param {Object} config to use.
     */
    useConfig(config: HybridConfig): void;
    /**
     * Get translators that support given source language and target language.
     *
     * @param from source language
     * @param to target language
     *
     * @returns available translators
     */
    getAvailableTranslatorsFor(from: string, to: string): HybridSupportedTranslators[];
    /**
     * Update hybrid translator config when language setting changed.
     *
     * @param from source language
     * @param to target language
     *
     * @returns new config
     */
    updateConfigFor(from: string, to: string): HybridConfig;
    /**
     * Detect language of given text.
     *
     * @param text text
     *
     * @returns Promise of language of given text
     */
    detect(text: string): Promise<any>;
    /**
     * Hybrid translate.
     *
     * @param text text to translate
     * @param from source language
     * @param to target language
     *
     * @returns result Promise
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
    pronounce(text: string, language: string, speed: PronunciationSpeed): Promise<any>;
    /**
     * Pause pronounce.
     */
    stopPronounce(): Promise<void>;
}
export default HybridTranslator;
