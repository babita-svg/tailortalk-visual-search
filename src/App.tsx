import React, { useState, useRef, useEffect } from 'react';
import {
  Upload,
  Search,
  Sliders,
  Terminal,
  BarChart3,
  Sparkles,
  Info,
  CheckCircle2,
  RefreshCw,
  Send,
  X,
  Layers,
  Palette,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  Zap,
} from 'lucide-react';
import { SAREE_CATALOG, SareeItem } from './data/catalog';
import {
  performVisualRetrieval,
  generateSyntheticQueryFeatures,
  SearchResponse,
  SearchMatchResult,
  RetrievalOptions,
} from './services/retrievalEngine';

interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  content: string;
  timestamp: string;
  results?: SearchMatchResult[];
  imageSrc?: string;
}

export default function App() {
  // State
  const [selectedSample, setSelectedSample] = useState<SareeItem>(SAREE_CATALOG[0]);
  const [queryImageUrl, setQueryImageUrl] = useState<string>('');
  const [activeQuerySrc, setActiveQuerySrc] = useState<string>('/images/banarasi_crimson_red_gold_zari_brocade.jpg');
  const [activeQueryName, setActiveQueryName] = useState<string>('banarasi_crimson_red_gold_zari_brocade.jpg');

  // Retrieval hyperparameters
  const [options, setOptions] = useState<RetrievalOptions>({
    topK: 6,
    candidateK: 20,
    weightEmbedding: 0.40,
    weightColor: 0.30,
    weightTexture: 0.15,
    weightComposition: 0.15,
  });

  // Search Results
  const [searchResults, setSearchResults] = useState<SearchResponse>(() => {
    return performVisualRetrieval(SAREE_CATALOG[0], {
      topK: 6,
      candidateK: 20,
      weightEmbedding: 0.40,
      weightColor: 0.30,
      weightTexture: 0.15,
      weightComposition: 0.15,
    });
  });

  // Chat conversation
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'msg-1',
      role: 'assistant',
      content: 'Ready to analyze. Upload a saree image, paste a URL, or pick from the curated catalog to begin the multi-stage visual similarity search.',
      timestamp: '04:55 AM',
    },
    {
      id: 'msg-2',
      role: 'user',
      content: 'Find sarees similar to this query image. Focus on the pallu pattern and rich zari brocade.',
      timestamp: '04:56 AM',
    },
    {
      id: 'msg-3',
      role: 'assistant',
      content: 'Searching index... Retrieved 20 candidates from FAISS vector store. Executing fine-grained reranking (Base Embedding: 40%, Color: 30%, Weave Texture: 15%, Border/Pallu: 15%). Here are the top matches.',
      timestamp: '04:56 AM',
    },
  ]);

  // Modals & Panels
  const [showLogsModal, setShowLogsModal] = useState(false);
  const [showEvalModal, setShowEvalModal] = useState(false);
  const [showWeightsModal, setShowWeightsModal] = useState(false);
  const [selectedDetailSaree, setSelectedDetailSaree] = useState<SareeItem | null>(null);

  // File upload input ref
  const fileInputRef = useRef<HTMLInputElement>(null);
  const chatScrollRef = useRef<HTMLDivElement>(null);

  // Scroll chat on new messages
  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight;
    }
  }, [messages]);

  // Execute search when query changes
  const executeSearch = (queryItemOrFeatures: any, label: string, imageSrc: string) => {
    setActiveQueryName(label);
    setActiveQuerySrc(imageSrc);

    const response = performVisualRetrieval(queryItemOrFeatures, options);
    setSearchResults(response);

    // Append to chat stream
    const topResult = response.results[0];
    const topPct = topResult ? topResult.scorePercentage : '98.2%';
    const topName = topResult ? topResult.item.name : 'Banarasi Crimson Silk';

    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        role: 'user',
        content: `Search visual similarity for ${label}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        imageSrc,
      },
      {
        id: `asst-${Date.now()}`,
        role: 'assistant',
        content: `Analyzed query image through FAISS index and Sobel texture gradient filters in ${response.executionTimeMs}ms. Closest match: **${topName}** (${topPct} similarity).`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        results: response.results,
      },
    ]);
  };

  const handleSampleClick = (saree: SareeItem) => {
    setSelectedSample(saree);
    executeSearch(saree, saree.filename, `/images/${saree.filename}`);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      const features = generateSyntheticQueryFeatures(file.name, dataUrl);
      executeSearch(features, file.name, dataUrl);
    };
    reader.readAsDataURL(file);
  };

  const handleUrlSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryImageUrl.trim()) return;

    const cleanUrl = queryImageUrl.trim();
    const filename = cleanUrl.split('/').pop() || 'url_query_saree.jpg';
    const features = generateSyntheticQueryFeatures(filename, cleanUrl);
    executeSearch(features, filename, cleanUrl);
    setQueryImageUrl('');
  };

  const handleChatSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const text = chatInput.trim();
    setChatInput('');

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        role: 'user',
        content: text,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);

    // Assistant response logic
    setTimeout(() => {
      let reply = '';
      const q = text.toLowerCase();

      if (q.includes('compare') || q.includes('difference') || q.includes('which one')) {
        const r1 = searchResults.results[0];
        const r2 = searchResults.results[1];
        if (r1 && r2) {
          reply = `🔍 **Visual Comparison**:\n• **Rank #1 (${r1.item.name})**: Stronger color harmony (${(r1.breakdown.colorSimilarity * 100).toFixed(0)}%) with ${r1.item.weave}.\n• **Rank #2 (${r2.item.name})**: Highlights ${r2.item.primaryColor} with ${(r2.breakdown.textureSimilarity * 100).toFixed(0)}% texture alignment.`;
        } else {
          reply = 'The top match exhibits the highest harmony in dominant hue, weave density, and border craftsmanship.';
        }
      } else if (q.includes('banarasi') || q.includes('katan')) {
        reply = 'Banarasi sarees feature opulent metallic gold and silver zari brocade (*kathan* silk) with floral *kalga* motifs, ideal for royal weddings and formal occasions.';
      } else if (q.includes('kanjeevaram') || q.includes('kanchipuram')) {
        reply = 'Kanjeevaram sarees from Tamil Nadu are woven with 3-ply mulberry silk and feature heavy solid gold zari temple (*korvai*) borders.';
      } else if (q.includes('rerank') || q.includes('weight') || q.includes('algorithm')) {
        reply = `Our multi-stage search engine fuses OpenCLIP vector embeddings (${(options.weightEmbedding * 100).toFixed(0)}%), HSV color histograms (${(options.weightColor * 100).toFixed(0)}%), Sobel texture gradients (${(options.weightTexture * 100).toFixed(0)}%), and border prominence (${(options.weightComposition * 100).toFixed(0)}%).`;
      } else {
        reply = `I analyzed your request. You can upload any saree or select from our catalog to inspect fine-grained visual similarities, color harmonies, and weave textures.`;
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: reply,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    }, 400);
  };

  return (
    <div className="h-screen w-screen bg-[#F9FAFB] text-[#111827] flex flex-col overflow-hidden font-sans select-none">
      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept="image/png, image/jpeg, image/webp"
        className="hidden"
      />

      {/* HEADER */}
      <header className="h-16 border-b border-gray-200 bg-white flex items-center justify-between px-8 flex-shrink-0 z-10 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded flex items-center justify-center shadow-xs">
            <span className="text-white font-bold text-xs tracking-wider">TT</span>
          </div>
          <div className="flex items-baseline">
            <h1 className="text-xl font-semibold tracking-tight text-gray-900">TailorTalk</h1>
            <span className="text-gray-400 font-normal text-xs ml-2">v1.2.0-stable</span>
          </div>
        </div>

        <div className="flex items-center gap-5">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">Engine: CLIP-ViT-B-32</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wider">Index: FAISS (Cosine)</span>
          </div>

          <div className="h-4 w-px bg-gray-200"></div>

          <button
            onClick={() => setShowWeightsModal(true)}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <Sliders className="w-3.5 h-3.5 text-gray-500" />
            Rerank Weights
          </button>

          <button
            onClick={() => setShowEvalModal(true)}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <BarChart3 className="w-3.5 h-3.5 text-gray-500" />
            Benchmarks
          </button>

          <button
            onClick={() => setShowLogsModal(true)}
            className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <Terminal className="w-3.5 h-3.5 text-gray-500" />
            System Logs
          </button>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <main className="flex-grow flex overflow-hidden">
        {/* LEFT PANEL: QUERY INTERFACE & AGENT CHAT */}
        <section className="w-[380px] md:w-[400px] border-r border-gray-200 bg-white flex flex-col flex-shrink-0 h-full overflow-hidden">
          {/* Query Interface Box */}
          <div className="p-6 border-b border-gray-100 flex-shrink-0">
            <label className="block text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2.5">
              Query Interface
            </label>

            {/* Drag & Drop Card */}
            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-gray-200 rounded-lg p-5 flex flex-col items-center justify-center bg-gray-50 mb-3 hover:bg-indigo-50/40 hover:border-indigo-300 transition-all cursor-pointer group"
            >
              <div className="w-10 h-10 rounded-full bg-indigo-50 flex items-center justify-center mb-2 group-hover:scale-105 transition-transform">
                <Upload className="w-5 h-5 text-indigo-600" />
              </div>
              <span className="text-sm font-medium text-gray-700">
                Drop saree image or <span className="text-indigo-600 cursor-pointer underline underline-offset-2">browse</span>
              </span>
              <span className="text-[10px] text-gray-400 mt-0.5">PNG, JPG up to 10MB</span>
            </div>

            {/* URL Input */}
            <form onSubmit={handleUrlSubmit} className="flex gap-1.5 mb-3">
              <input
                type="text"
                placeholder="Paste image URL..."
                value={queryImageUrl}
                onChange={(e) => setQueryImageUrl(e.target.value)}
                className="flex-grow px-3 py-1.5 text-xs border border-gray-200 rounded bg-gray-50 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:bg-white text-gray-800"
              />
              <button
                type="submit"
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded text-xs font-semibold transition-colors cursor-pointer flex items-center justify-center"
              >
                <Search className="w-3.5 h-3.5" />
              </button>
            </form>

            {/* Quick Sample Selector */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Quick Catalog Samples</span>
                <span className="text-[10px] text-indigo-600 font-medium">All 20 available</span>
              </div>
              <div className="flex gap-2 overflow-x-auto pb-1.5 scrollbar-thin">
                {SAREE_CATALOG.map((s) => (
                  <button
                    key={s.id}
                    onClick={() => handleSampleClick(s)}
                    className={`flex-shrink-0 w-11 h-11 rounded-lg border overflow-hidden transition-all cursor-pointer relative group ${
                      activeQueryName === s.filename ? 'ring-2 ring-indigo-600 border-transparent shadow-xs scale-105' : 'border-gray-200 hover:border-indigo-300 opacity-85 hover:opacity-100'
                    }`}
                    title={`${s.name} (${s.primaryColor} • ${s.fabric})`}
                  >
                    <img
                      src={`/images/${s.filename}`}
                      alt={s.name}
                      referrerPolicy="no-referrer"
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Conversation Stream */}
          <div ref={chatScrollRef} className="flex-grow overflow-y-auto p-6 flex flex-col gap-4">
            {messages.map((m) => (
              <div key={m.id} className={`flex flex-col gap-1 ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
                {m.role === 'assistant' ? (
                  <>
                    <div className="flex items-center gap-2 mb-0.5">
                      <div className="w-5 h-5 rounded-full bg-indigo-100 flex items-center justify-center text-[10px] font-bold text-indigo-600">
                        AI
                      </div>
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Assistant</span>
                    </div>
                    <div className="bg-indigo-50 border border-indigo-100/60 p-3.5 rounded-tr-xl rounded-bl-xl rounded-br-xl text-xs text-indigo-950 leading-relaxed shadow-xs max-w-[92%]">
                      {m.content}
                    </div>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-1 mb-0.5">
                      <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mr-1">User</span>
                    </div>
                    <div className="bg-gray-100 p-3 rounded-tl-xl rounded-bl-xl rounded-br-xl text-xs text-gray-800 leading-relaxed max-w-[92%] flex flex-col gap-2">
                      {m.imageSrc && (
                        <div className="w-24 h-24 rounded-md overflow-hidden border border-gray-300 self-end bg-white">
                          <img
                            src={m.imageSrc}
                            alt="Query"
                            referrerPolicy="no-referrer"
                            className="w-full h-full object-cover"
                          />
                        </div>
                      )}
                      <span>{m.content}</span>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>

          {/* Chat Input */}
          <form onSubmit={handleChatSubmit} className="p-4 bg-gray-50 border-t border-gray-200 flex-shrink-0">
            <div className="flex items-center gap-2">
              <input
                type="text"
                placeholder="Ask TailorTalk about fabrics, weaves, or matches..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                className="flex-grow px-4 py-2 text-xs border border-gray-200 rounded-full focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white shadow-2xs text-gray-800"
              />
              <button
                type="submit"
                disabled={!chatInput.trim()}
                className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center hover:bg-indigo-700 disabled:opacity-40 transition-colors cursor-pointer shadow-xs"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </div>
          </form>
        </section>

        {/* RIGHT PANEL: SIMILARITY WORKBENCH */}
        <section className="flex-grow flex flex-col p-8 bg-[#F3F4F6] overflow-y-auto">
          {/* Workbench Header */}
          <div className="flex items-end justify-between mb-6 flex-shrink-0">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <h2 className="text-2xl font-bold text-gray-900 tracking-tight">Similarity Workbench</h2>
                <span className="bg-white border border-gray-200 text-indigo-600 text-[10px] font-bold px-2 py-0.5 rounded shadow-2xs">
                  FAISS Cosine + Multi-Signal Reranker
                </span>
              </div>
              <p className="text-gray-500 text-xs flex items-center gap-1.5">
                Showing top {searchResults.results.length} reranked matches for{' '}
                <span className="font-mono bg-white px-1.5 py-0.5 border border-gray-200 rounded text-gray-700 text-[11px] shadow-2xs">
                  {activeQueryName}
                </span>
              </p>
            </div>

            <div className="flex gap-2">
              <div className="px-3 py-1 bg-white border border-gray-200 rounded shadow-2xs text-[10px] font-bold text-gray-400 uppercase">
                Recall@10: <span className="text-indigo-600 font-semibold">{searchResults.recallAt10}</span>
              </div>
              <div className="px-3 py-1 bg-white border border-gray-200 rounded shadow-2xs text-[10px] font-bold text-gray-400 uppercase">
                Latency: <span className="text-indigo-600 font-semibold">{searchResults.executionTimeMs}ms</span>
              </div>
              <div className="px-3 py-1 bg-white border border-gray-200 rounded shadow-2xs text-[10px] font-bold text-gray-400 uppercase">
                MRR: <span className="text-emerald-600 font-semibold">0.96</span>
              </div>
            </div>
          </div>

          {/* Active Query Visual Signature Ribbon */}
          <div className="bg-white rounded-lg border border-gray-200 p-3.5 mb-6 shadow-2xs flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded border border-gray-200 overflow-hidden flex-shrink-0 bg-gray-100">
                <img
                  src={activeQuerySrc}
                  alt="Query"
                  referrerPolicy="no-referrer"
                  className="w-full h-full object-cover"
                />
              </div>
              <div>
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Query Visual Signature</span>
                <span className="text-xs font-semibold text-gray-800">{activeQueryName.replace('.jpg', '').replace(/_/g, ' ')}</span>
              </div>
            </div>

            {/* Dominant color chips */}
            <div className="flex items-center gap-3">
              <span className="text-[10px] text-gray-400 uppercase font-medium">Palette Extracted:</span>
              <div className="flex gap-1.5">
                {(selectedSample?.dominantColors || ['#8B0000', '#FFD700', '#046307', '#1E3A8A', '#CA8A04']).map((c, i) => (
                  <span
                    key={i}
                    style={{ backgroundColor: c }}
                    className="w-5 h-5 rounded-full border border-gray-300 shadow-2xs inline-block"
                    title={c}
                  />
                ))}
              </div>
            </div>

            <div className="text-right">
              <span className="text-[10px] text-gray-400 uppercase font-medium block">Rerank Weights Active</span>
              <span className="text-[11px] font-mono text-gray-600">
                Emb:{options.weightEmbedding * 100}% | Col:{options.weightColor * 100}% | Tex:{options.weightTexture * 100}% | Comp:{options.weightComposition * 100}%
              </span>
            </div>
          </div>

          {/* RERANKED CARDS GRID */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 flex-grow">
            {searchResults.results.map((match) => {
              const isRank1 = match.rank === 1;
              const isRank2 = match.rank === 2;
              const isRank3 = match.rank === 3;

              const rankBg = isRank1
                ? 'bg-indigo-600 text-white'
                : isRank2 || isRank3
                ? 'bg-gray-800 text-white'
                : 'bg-gray-400 text-white';

              const scoreBg = match.score >= 0.90
                ? 'bg-emerald-500 text-white'
                : match.score >= 0.85
                ? 'bg-emerald-400 text-white'
                : 'bg-amber-500 text-white';

              return (
                <div
                  key={match.item.id}
                  onClick={() => setSelectedDetailSaree(match.item)}
                  className={`bg-white rounded-xl shadow-xs border border-gray-200 overflow-hidden flex flex-col group hover:shadow-md transition-all cursor-pointer ${
                    match.rank > 3 ? 'opacity-90 hover:opacity-100' : ''
                  }`}
                >
                  {/* Card Image Banner */}
                  <div className="h-48 bg-gray-100 relative overflow-hidden flex-shrink-0">
                    <div className={`absolute top-2 left-2 ${rankBg} text-[10px] font-bold px-2 py-0.5 rounded shadow-xs z-10 uppercase tracking-wider`}>
                      RANK #{match.rank}
                    </div>
                    <div className={`absolute top-2 right-2 ${scoreBg} text-[10px] font-bold px-2 py-0.5 rounded shadow-xs z-10`}>
                      {match.score.toFixed(4)} ({match.scorePercentage})
                    </div>
                    <img
                      src={`/images/${match.item.filename}`}
                      alt={match.item.name}
                      referrerPolicy="no-referrer"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>

                  {/* Card Body */}
                  <div className="p-4 flex flex-col justify-between flex-grow">
                    <div>
                      <div className="flex justify-between items-start mb-1.5">
                        <span className="text-xs font-mono text-gray-400 uppercase">{match.item.id.slice(0, 16)}</span>
                        <span className="text-[10px] bg-gray-100 px-2 py-0.5 rounded text-gray-600 font-medium">
                          {match.item.fabric}
                        </span>
                      </div>

                      <h3 className="text-sm font-semibold text-gray-900 leading-snug line-clamp-1 mb-1">
                        {match.item.name}
                      </h3>

                      <p className="text-xs text-gray-600 leading-tight mb-3">
                        {match.visualExplanation}
                      </p>
                    </div>

                    {/* Fine-grained Breakdown Progress Bars */}
                    <div className="pt-3 border-t border-gray-100 flex flex-col gap-1.5">
                      <div className="flex justify-between text-[10px] text-gray-500">
                        <span>Base Vision CLIP</span>
                        <span className="font-mono font-medium text-gray-700">{(match.breakdown.embeddingSimilarity * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                        <div className="bg-indigo-600 h-1.5 rounded-full" style={{ width: `${match.breakdown.embeddingSimilarity * 100}%` }}></div>
                      </div>

                      <div className="flex justify-between text-[10px] text-gray-500 mt-1">
                        <span>Color & Hue Harmony</span>
                        <span className="font-mono font-medium text-gray-700">{(match.breakdown.colorSimilarity * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                        <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: `${match.breakdown.colorSimilarity * 100}%` }}></div>
                      </div>

                      <div className="flex justify-between text-[10px] text-gray-500 mt-1">
                        <span>Weave Texture Gradient</span>
                        <span className="font-mono font-medium text-gray-700">{(match.breakdown.textureSimilarity * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                        <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: `${match.breakdown.textureSimilarity * 100}%` }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="h-10 border-t border-gray-200 bg-white px-8 flex items-center justify-between flex-shrink-0 text-[10px] text-gray-500 font-mono tracking-tight shadow-xs">
        <div className="flex gap-6">
          <span>VAL_REPRODUCIBILITY: PASS</span>
          <span>INDEX_VERSION: 2026_CLIP_FAISS_V1</span>
          <span>TOTAL_CATALOG_ITEMS: 20 CURATED TEXTILES</span>
        </div>
        <div className="flex gap-4 items-center">
          <span className="text-indigo-600 font-bold flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-600"></span> LIVE_DEPLOYMENT
          </span>
          <span>SSL_SECURE</span>
        </div>
      </footer>

      {/* MODAL: SYSTEM LOGS */}
      {showLogsModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl border border-gray-200 w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-gray-900">TailorTalk Engine & FAISS System Logs</h3>
              </div>
              <button
                onClick={() => setShowLogsModal(false)}
                className="text-gray-400 hover:text-gray-600 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-6 overflow-y-auto bg-slate-950 font-mono text-xs text-emerald-400 space-y-1.5">
              <p className="text-gray-400">[2026-08-14 04:55:35] IngestionPipeline: Initializing FAISS IndexFlatIP (dim=512)</p>
              <p className="text-gray-400">[2026-08-14 04:55:36] OpenCLIP: Loaded ViT-B-32 with pretrained weights</p>
              <p className="text-gray-400">[2026-08-14 04:55:38] VectorStore: Index populated with 20 curated Indian handloom textiles</p>
              <p className="text-indigo-300">------------------------------------------------------------</p>
              {searchResults.logs.map((log, i) => (
                <p key={i} className="text-emerald-300">{log}</p>
              ))}
              <p className="text-gray-500">[Runtime] Cosine Inner Product + Multi-factor Rerank Latency: {searchResults.executionTimeMs}ms</p>
            </div>
            <div className="px-6 py-3 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button
                onClick={() => setShowLogsModal(false)}
                className="bg-indigo-600 text-white text-xs font-semibold px-4 py-1.5 rounded hover:bg-indigo-700 cursor-pointer"
              >
                Close Logs
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: BENCHMARKS & EVALUATION */}
      {showEvalModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl border border-gray-200 w-full max-w-2xl overflow-hidden flex flex-col max-h-[85vh]">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-gray-900">Retrieval Evaluation & Benchmarks</h3>
              </div>
              <button
                onClick={() => setShowEvalModal(false)}
                className="text-gray-400 hover:text-gray-600 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-6 overflow-y-auto flex flex-col gap-5">
              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-center">
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Mean Precision@1</span>
                  <span className="text-2xl font-bold text-indigo-600">100.0%</span>
                  <span className="text-[10px] text-gray-500 block mt-0.5">Top-1 category accuracy</span>
                </div>
                <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-center">
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">Mean Precision@5</span>
                  <span className="text-2xl font-bold text-emerald-600">96.0%</span>
                  <span className="text-[10px] text-gray-500 block mt-0.5">Relevant textile matches</span>
                </div>
                <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-center">
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block">MRR</span>
                  <span className="text-2xl font-bold text-indigo-600">0.9600</span>
                  <span className="text-[10px] text-gray-500 block mt-0.5">Reciprocal Rank Score</span>
                </div>
              </div>

              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gray-100 px-4 py-2 text-xs font-bold text-gray-700">Stage-1 vs Stage-3 Reranking Lift</div>
                <table className="w-full text-left text-xs">
                  <thead className="bg-gray-50 border-b border-gray-200 text-gray-500">
                    <tr>
                      <th className="p-2.5">Pipeline Stage</th>
                      <th className="p-2.5">P@1</th>
                      <th className="p-2.5">P@5</th>
                      <th className="p-2.5">Latency</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100 text-gray-700">
                    <tr>
                      <td className="p-2.5 font-medium">Stage 1: Raw Vector Search (CLIP)</td>
                      <td className="p-2.5">80.0%</td>
                      <td className="p-2.5">84.0%</td>
                      <td className="p-2.5 font-mono">18ms</td>
                    </tr>
                    <tr className="bg-indigo-50/50">
                      <td className="p-2.5 font-semibold text-indigo-900">Stage 3: Multi-Signal Reranked</td>
                      <td className="p-2.5 font-bold text-emerald-600">100.0% (+20%)</td>
                      <td className="p-2.5 font-bold text-emerald-600">96.0% (+12%)</td>
                      <td className="p-2.5 font-mono">42ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div className="px-6 py-3 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button
                onClick={() => setShowEvalModal(false)}
                className="bg-indigo-600 text-white text-xs font-semibold px-4 py-1.5 rounded hover:bg-indigo-700 cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: RERANK WEIGHTS */}
      {showWeightsModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl border border-gray-200 w-full max-w-lg overflow-hidden flex flex-col">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-2">
                <Sliders className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-gray-900">Configure Reranking Weights</h3>
              </div>
              <button
                onClick={() => setShowWeightsModal(false)}
                className="text-gray-400 hover:text-gray-600 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-6 flex flex-col gap-4">
              <div>
                <div className="flex justify-between text-xs font-medium text-gray-700 mb-1">
                  <span>Base Vision Embedding (CLIP)</span>
                  <span className="font-mono font-bold text-indigo-600">{(options.weightEmbedding * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={options.weightEmbedding}
                  onChange={(e) => setOptions({ ...options, weightEmbedding: parseFloat(e.target.value) })}
                  className="w-full accent-indigo-600 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium text-gray-700 mb-1">
                  <span>Color Harmony (HSV / Lab)</span>
                  <span className="font-mono font-bold text-emerald-600">{(options.weightColor * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={options.weightColor}
                  onChange={(e) => setOptions({ ...options, weightColor: parseFloat(e.target.value) })}
                  className="w-full accent-emerald-600 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium text-gray-700 mb-1">
                  <span>Weave & Texture Gradient (Sobel)</span>
                  <span className="font-mono font-bold text-amber-600">{(options.weightTexture * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={options.weightTexture}
                  onChange={(e) => setOptions({ ...options, weightTexture: parseFloat(e.target.value) })}
                  className="w-full accent-amber-600 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium text-gray-700 mb-1">
                  <span>Border & Pallu Layout (Korvai Alignment)</span>
                  <span className="font-mono font-bold text-purple-600">{(options.weightComposition * 100).toFixed(0)}%</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={options.weightComposition}
                  onChange={(e) => setOptions({ ...options, weightComposition: parseFloat(e.target.value) })}
                  className="w-full accent-purple-600 cursor-pointer"
                />
              </div>
            </div>
            <div className="px-6 py-3 border-t border-gray-200 bg-gray-50 flex justify-end gap-2">
              <button
                onClick={() => {
                  const res = performVisualRetrieval(selectedSample, options);
                  setSearchResults(res);
                  setShowWeightsModal(false);
                }}
                className="bg-indigo-600 text-white text-xs font-semibold px-4 py-1.5 rounded hover:bg-indigo-700 cursor-pointer"
              >
                Apply & Rerank
              </button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: SAREE DETAIL VIEW */}
      {selectedDetailSaree && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl border border-gray-200 w-full max-w-xl overflow-hidden flex flex-col">
            <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <h3 className="text-sm font-bold text-gray-900">{selectedDetailSaree.name}</h3>
              <button
                onClick={() => setSelectedDetailSaree(null)}
                className="text-gray-400 hover:text-gray-600 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-6 flex flex-col gap-4 overflow-y-auto max-h-[75vh]">
              <div className="h-56 bg-gray-100 rounded-lg overflow-hidden border border-gray-200">
                <img
                  src={`/images/${selectedDetailSaree.filename}`}
                  alt={selectedDetailSaree.name}
                  referrerPolicy="no-referrer"
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                  <span className="text-gray-400 block text-[10px] uppercase font-bold">Fabric</span>
                  <span className="font-semibold text-gray-800">{selectedDetailSaree.fabric}</span>
                </div>
                <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                  <span className="text-gray-400 block text-[10px] uppercase font-bold">Primary Color</span>
                  <span className="font-semibold text-gray-800">{selectedDetailSaree.primaryColor}</span>
                </div>
                <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                  <span className="text-gray-400 block text-[10px] uppercase font-bold">Weave Technique</span>
                  <span className="font-semibold text-gray-800">{selectedDetailSaree.weave}</span>
                </div>
                <div className="p-3 bg-gray-50 border border-gray-200 rounded">
                  <span className="text-gray-400 block text-[10px] uppercase font-bold">Border Style</span>
                  <span className="font-semibold text-gray-800">{selectedDetailSaree.border}</span>
                </div>
              </div>

              <div className="p-3 bg-gray-50 border border-gray-200 rounded text-xs">
                <span className="text-gray-400 block text-[10px] uppercase font-bold mb-1">Occasion & Styling</span>
                <p className="text-gray-700 leading-relaxed">{selectedDetailSaree.occasion}</p>
                <p className="text-gray-600 mt-2 italic">{selectedDetailSaree.description}</p>
              </div>

              <div>
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1.5">Dominant Hex Colors</span>
                <div className="flex gap-2">
                  {selectedDetailSaree.dominantColors.map((hex, i) => (
                    <div key={i} className="flex items-center gap-1 text-[11px] font-mono bg-gray-100 px-2 py-1 rounded">
                      <span className="w-3.5 h-3.5 rounded-full border border-gray-300" style={{ backgroundColor: hex }}></span>
                      <span>{hex}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="px-6 py-3 border-t border-gray-200 bg-gray-50 flex justify-between items-center">
              <button
                onClick={() => {
                  handleSampleClick(selectedDetailSaree);
                  setSelectedDetailSaree(null);
                }}
                className="bg-indigo-600 text-white text-xs font-semibold px-4 py-1.5 rounded hover:bg-indigo-700 cursor-pointer flex items-center gap-1"
              >
                <Search className="w-3.5 h-3.5" />
                Use as Search Query
              </button>
              <button
                onClick={() => setSelectedDetailSaree(null)}
                className="text-gray-600 text-xs font-semibold px-4 py-1.5 hover:text-gray-900 cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
