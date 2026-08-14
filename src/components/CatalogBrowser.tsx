import React, { useState, useMemo } from 'react';
import { SAREE_CATALOG, SareeItem } from '../data/catalog';
import { SareeImage } from './SareeImage';
import { Search, ExternalLink, Filter, ChevronLeft, ChevronRight, ShoppingBag, Tag, CheckCircle2 } from 'lucide-react';

interface CatalogBrowserProps {
  onSelectSaree: (saree: SareeItem) => void;
  onOpenDetail: (saree: SareeItem) => void;
}

export const CatalogBrowser: React.FC<CatalogBrowserProps> = ({ onSelectSaree, onOpenDetail }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedStockFilter, setSelectedStockFilter] = useState<'all' | 'in_stock' | 'out_of_stock'>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 24;

  const categories = useMemo(() => {
    const set = new Set<string>();
    SAREE_CATALOG.forEach((item) => set.add(item.category));
    return ['All', ...Array.from(set).sort()];
  }, []);

  const filteredItems = useMemo(() => {
    return SAREE_CATALOG.filter((item) => {
      // Search filter
      const matchesSearch =
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (item.sku && item.sku.toLowerCase().includes(searchTerm.toLowerCase())) ||
        item.fabric.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.primaryColor.toLowerCase().includes(searchTerm.toLowerCase());

      // Category filter
      const matchesCat = selectedCategory === 'All' || item.category === selectedCategory;

      // Stock filter
      let matchesStock = true;
      if (selectedStockFilter === 'in_stock') {
        matchesStock = (item.stock || 0) > 0;
      } else if (selectedStockFilter === 'out_of_stock') {
        matchesStock = (item.stock || 0) <= 0;
      }

      return matchesSearch && matchesCat && matchesStock;
    });
  }, [searchTerm, selectedCategory, selectedStockFilter]);

  const totalPages = Math.ceil(filteredItems.length / pageSize) || 1;
  const paginatedItems = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredItems.slice(start, start + pageSize);
  }, [filteredItems, currentPage, pageSize]);

  return (
    <div className="flex flex-col h-full bg-[#F9FAFB] overflow-hidden">
      {/* Top Controls Bar */}
      <div className="p-6 bg-white border-b border-gray-200 flex-shrink-0 shadow-2xs">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-gray-900 tracking-tight">Authoritative Saree Catalogue</h2>
              <span className="bg-indigo-50 text-indigo-700 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-indigo-200">
                {SAREE_CATALOG.length} Verified Products
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Explore inventory, pricing, SKU mappings, and launch instant visual searches across the collection.
            </p>
          </div>

          {/* Quick diagnostic stats badge */}
          <div className="flex items-center gap-2 text-xs font-mono bg-gray-50 p-2 rounded-lg border border-gray-200">
            <span className="text-emerald-700 font-semibold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> 100% Ingested
            </span>
            <span className="text-gray-300">|</span>
            <span className="text-gray-600">FAISS Vectors: {SAREE_CATALOG.length}</span>
          </div>
        </div>

        {/* Filter Toolbar */}
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <div className="relative flex-grow max-w-md">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by product name, SKU, color, or fabric..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full pl-9 pr-4 py-1.5 text-xs bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:bg-white text-gray-800"
            />
          </div>

          {/* Category Dropdown */}
          <div className="flex items-center gap-1.5 text-xs">
            <Filter className="w-3.5 h-3.5 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setCurrentPage(1);
              }}
              className="px-2.5 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-700 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'All' ? 'All Weaves / Types' : cat}
                </option>
              ))}
            </select>
          </div>

          {/* Stock Filter */}
          <select
            value={selectedStockFilter}
            onChange={(e) => {
              setSelectedStockFilter(e.target.value as any);
              setCurrentPage(1);
            }}
            className="px-2.5 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-700 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="all">All Inventory</option>
            <option value="in_stock">In Stock Only</option>
            <option value="out_of_stock">Out of Stock</option>
          </select>

          <span className="text-xs text-gray-500 ml-auto font-medium">
            Showing {filteredItems.length === 0 ? 0 : (currentPage - 1) * pageSize + 1} -{' '}
            {Math.min(currentPage * pageSize, filteredItems.length)} of {filteredItems.length} products
          </span>
        </div>
      </div>

      {/* Grid Display */}
      <div className="flex-grow p-6 overflow-y-auto">
        {paginatedItems.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-64 text-center">
            <ShoppingBag className="w-10 h-10 text-gray-300 mb-2" />
            <span className="text-sm font-semibold text-gray-600">No catalogue products match your filter</span>
            <span className="text-xs text-gray-400 mt-1">Try searching for a different keyword or resetting filters.</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {paginatedItems.map((item) => (
              <div
                key={item.id}
                onClick={() => onOpenDetail(item)}
                className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-2xs hover:shadow-md transition-all flex flex-col cursor-pointer group"
              >
                {/* Image Container */}
                <div className="h-44 bg-gray-100 relative overflow-hidden">
                  <SareeImage
                    src={item.imageUrl || `/images/${item.filename}`}
                    alt={item.name}
                    dominantColors={item.dominantColors}
                    fabric={item.fabric}
                    primaryColor={item.primaryColor}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-xs text-white text-[9px] font-mono px-1.5 py-0.5 rounded">
                    {item.sku || 'SKU'}
                  </div>
                  {item.stock !== undefined && item.stock > 0 ? (
                    <div className="absolute top-2 right-2 bg-emerald-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow-xs">
                      {item.stock} in stock
                    </div>
                  ) : (
                    <div className="absolute top-2 right-2 bg-gray-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded">
                      Out of stock
                    </div>
                  )}
                </div>

                {/* Details */}
                <div className="p-3.5 flex flex-col justify-between flex-grow">
                  <div>
                    <span className="text-[10px] text-indigo-600 font-semibold uppercase tracking-wider block mb-1">
                      {item.category} • {item.fabric}
                    </span>
                    <h4 className="text-xs font-bold text-gray-900 line-clamp-2 leading-tight mb-2 group-hover:text-indigo-600 transition-colors">
                      {item.name}
                    </h4>
                  </div>

                  <div>
                    {/* Price */}
                    <div className="flex items-baseline gap-1.5 mb-2.5">
                      {item.discountedPrice ? (
                        <>
                          <span className="text-sm font-bold text-gray-900">₹{item.discountedPrice.toLocaleString()}</span>
                          {item.retailPrice && item.retailPrice > item.discountedPrice && (
                            <span className="text-[10px] text-gray-400 line-through">₹{item.retailPrice.toLocaleString()}</span>
                          )}
                        </>
                      ) : item.retailPrice ? (
                        <span className="text-sm font-bold text-gray-900">₹{item.retailPrice.toLocaleString()}</span>
                      ) : (
                        <span className="text-xs text-gray-500 font-medium">Price on request</span>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-1.5 pt-2 border-t border-gray-100">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectSaree(item);
                        }}
                        className="flex-grow py-1.5 px-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-[11px] font-semibold rounded text-center transition-colors cursor-pointer flex items-center justify-center gap-1"
                        title="Run visual similarity search using this saree"
                      >
                        <Search className="w-3 h-3" />
                        Search Similar
                      </button>

                      {item.websiteLink && (
                        <a
                          href={item.websiteLink}
                          target="_blank"
                          rel="noreferrer"
                          onClick={(e) => e.stopPropagation()}
                          className="py-1.5 px-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded transition-colors"
                          title="View on store website"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Pagination Footer */}
      {totalPages > 1 && (
        <div className="p-3.5 bg-white border-t border-gray-200 flex items-center justify-between flex-shrink-0 px-6">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            className="flex items-center gap-1 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs font-semibold text-gray-700 hover:bg-gray-100 disabled:opacity-40 cursor-pointer"
          >
            <ChevronLeft className="w-3.5 h-3.5" /> Previous
          </button>

          <span className="text-xs text-gray-600 font-medium">
            Page {currentPage} of {totalPages}
          </span>

          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            className="flex items-center gap-1 px-3 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs font-semibold text-gray-700 hover:bg-gray-100 disabled:opacity-40 cursor-pointer"
          >
            Next <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
};
