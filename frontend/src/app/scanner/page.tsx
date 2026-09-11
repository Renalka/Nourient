"use client";
import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from '@/lib/api';
import { useRouter } from "next/navigation";
import SidebarLayout from '@/components/SidebarLayout';
import AvatarMenu from '@/components/AvatarMenu';
import Breadcrumbs from '@/components/Breadcrumbs';
import { getScanHistory, saveScanHistory, ScanItem } from '@/lib/firebase/history';

const getGrade = (score: number) => {
  if (score >= 90) return { letter: 'A', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200', circle: 'border-green-500', fill: 'bg-green-500' };
  if (score >= 75) return { letter: 'B', color: 'text-green-500', bg: 'bg-green-50', border: 'border-green-200', circle: 'border-green-400', fill: 'bg-green-400' };
  if (score >= 60) return { letter: 'C', color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200', circle: 'border-yellow-500', fill: 'bg-yellow-500' };
  if (score >= 40) return { letter: 'D', color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200', circle: 'border-orange-500', fill: 'bg-orange-500' };
  return { letter: 'E', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200', circle: 'border-red-500', fill: 'bg-red-500' };
};

const getFormulationTier = (score: number) => {
  if (score >= 80) return { label: 'Clean & Wholesome', color: 'text-brand', bg: 'bg-brand-light', fill: 'bg-brand' };
  if (score >= 40) return { label: 'Fair Formulation', color: 'text-yellow-700', bg: 'bg-yellow-50', fill: 'bg-yellow-500' };
  return { label: 'Poor Formulation', color: 'text-red-700', bg: 'bg-red-50', fill: 'bg-red-500' };
};

export default function ScannerPage() {
  const { user, loading, getToken } = useAuth();
  const router = useRouter();

  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [file2, setFile2] = useState<File | null>(null);
  const [previewUrl2, setPreviewUrl2] = useState<string | null>(null);
  const [step, setStep] = useState<1|2|3|4>(1);
  const [scanMode, setScanMode] = useState<'ingredients' | 'front' | 'nutrition' | 'claims'>('ingredients'); // 1: Capture, 2: Review, 3: Analyze, 4: Results
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [addingToBasket, setAddingToBasket] = useState(false);
  const [basketMsg, setBasketMsg] = useState("");
  const [isEditingName, setIsEditingName] = useState(false);
  const [editNameValue, setEditNameValue] = useState("");

  const uploadInputRef = useRef<HTMLInputElement>(null);
  const uploadInputRef2 = useRef<HTMLInputElement>(null);
  
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [activeClaimsTab, setActiveClaimsTab] = useState<'front' | 'back'>('front');
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [progress, setProgress] = useState(0);
  const [progressText, setProgressText] = useState("Scanning image topology...");

  useEffect(() => {
    if (step === 3) {
      setProgress(0);
      setProgressText("Scanning image topology...");
      
      const texts = [
        { time: 0, text: "Scanning image topology..." },
        { time: 2000, text: "Extracting raw ingredients..." },
        { time: 4000, text: "Identifying hidden additives & INS codes..." },
        { time: 6000, text: "Cross-referencing TrueLabel database..." },
        { time: 8000, text: "Computing final nutritional profile..." }
      ];

      const timeouts = texts.map(t => 
        setTimeout(() => setProgressText(t.text), t.time)
      );

      const interval = setInterval(() => {
        setProgress(prev => Math.min(prev + 0.475, 95));
      }, 50);

      return () => {
        timeouts.forEach(clearTimeout);
        clearInterval(interval);
      };
    }
  }, [step]);



  useEffect(() => {
    return () => { stopCamera(); };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      setIsCameraActive(true);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Camera error:", err);
      alert("Could not access camera. Please check permissions or use the upload button.");
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      const MAX_WIDTH = 1200;
      const MAX_HEIGHT = 1600;
      let width = video.videoWidth;
      let height = video.videoHeight;

      if (width > height) {
        if (width > MAX_WIDTH) {
          height *= MAX_WIDTH / width;
          width = MAX_WIDTH;
        }
      } else {
        if (height > MAX_HEIGHT) {
          width *= MAX_HEIGHT / height;
          height = MAX_HEIGHT;
        }
      }

      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          if (blob) {
            const capturedFile = new File([blob], "capture.jpg", { type: "image/jpeg" });
            if (scanMode === 'claims') {
              if (activeClaimsTab === 'back') {
                setFile2(capturedFile);
                setPreviewUrl2(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file) setStep(2);
                else setActiveClaimsTab('front');
              } else {
                setFile(capturedFile);
                setPreviewUrl(URL.createObjectURL(capturedFile));
                stopCamera();
                if (file2) setStep(2);
                else setActiveClaimsTab('back'); // Auto-advance tab!
              }
            } else {
              setFile(capturedFile);
              setPreviewUrl(URL.createObjectURL(capturedFile));
              stopCamera();
              setStep(2);
            }
          }
        }, 'image/jpeg', 0.7);
      }
    }
  };

  const compressImage = (file: File): Promise<File> => {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = URL.createObjectURL(file);
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const MAX_WIDTH = 1200;
        const MAX_HEIGHT = 1600;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
          }
        } else {
          if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;
          }
        }
        canvas.width = width;
        canvas.height = height;
        ctx?.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => {
            if(blob) {
                const newName = file.name.replace(/\.[^/.]+$/, "") + ".jpg";
                resolve(new File([blob], newName, { type: 'image/jpeg' }));
            } else {
                resolve(file); // fallback
            }
        }, 'image/jpeg', 0.7);
      };
      img.onerror = () => resolve(file); // fallback
    });
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile(compressed);
      setPreviewUrl(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file2) setStep(2);
        else setActiveClaimsTab('back');
      } else {
        setStep(2);
      }
    }
  };

  const handleFile2Change = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      const compressed = await compressImage(selectedFile);
      setFile2(compressed);
      setPreviewUrl2(URL.createObjectURL(compressed));
      if (scanMode === 'claims') {
        if (file) setStep(2);
        else setActiveClaimsTab('front');
      } else {
        setStep(2);
      }
    }
  };

  const handleRetake = () => {
    setFile(null);
    setPreviewUrl(null);
    setFile2(null);
    setPreviewUrl2(null);
    setStep(1);
    setError(null);
  };

  const handleNameSave = async () => {
    setIsEditingName(false);
    const updatedName = editNameValue.trim();
    if (!updatedName) return;

    // Update local state
    const updatedResult = { ...result };
    if (updatedResult.extracted_data) {
        updatedResult.extracted_data.name = updatedName;
    } else {
        updatedResult.name = updatedName;
    }
    setResult(updatedResult);

    // Update Firestore history
    if (user) {
        try {
            const history = await getScanHistory(user.uid);
            if (history.length > 0) {
                // The first item is usually the current scan
                history[0].name = updatedName;
                await saveScanHistory(user.uid, history);
            }
        } catch (e) {
            console.error("Failed to update name in history", e);
        }
    }
  };

  const processImage = async (isEnhanced = false) => {
    if (!file) return;
    if (scanMode === 'claims' && !file2) {
      setError("Please capture both the front and back of the pack to verify claims.");
      return;
    }
    setStep(3); // Analyzing
    setError(null);

    const formData = new FormData();
    if (scanMode === 'claims') {
      formData.append('front_file', file);
      if (file2) formData.append('back_file', file2);
    } else {
      formData.append('file', file);
    }

    try {
      const token = await getToken();

      const endpoint = scanMode === 'claims'
        ? apiUrl('/api/v1/orchestrate/claims-scanner')
        : scanMode === 'front'
        ? apiUrl('/api/v1/orchestrate/front-scanner')
        : scanMode === 'nutrition'
            ? apiUrl('/api/v1/orchestrate/nutrition-scanner')
            : (isEnhanced 
                ? apiUrl('/api/v1/orchestrate/enhanced_scanner')
                : apiUrl('/api/v1/orchestrate/scanner'));

      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      // Step 1: ADK Orchestrator
      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
           throw new Error("Your session expired. Please refresh the page or log in again.");
        }
        let errBody = response.statusText;
        try {
          const errJson = await response.json();
          errBody = errJson.detail || JSON.stringify(errJson);
        } catch {
          errBody = await response.text() || response.statusText;
        }
        console.error(`Orchestration failed: ${errBody}`);
        throw new Error("Our servers are currently experiencing issues analyzing this product. Please try again in a few moments.");
      }

      const data = await response.json();
      
      // Explicit AI Rejections (Blurry, Invalid Image, No Data)
      if (data.extracted_data?.error) {
        throw new Error(data.extracted_data.error_message || "Could not read the image.");
      }

      // Option 4: Smart Fallback Naming using top ingredient
      let finalName = data.extracted_data?.name || data.name || '';
      const extractedIngredients = data.extracted_data?.ingredients || [];
      if ((!finalName || finalName.trim() === '') && extractedIngredients.length > 0) {
        const firstIng = extractedIngredients[0].name || '';
        if (firstIng) {
          const capitalized = firstIng.charAt(0).toUpperCase() + firstIng.slice(1).toLowerCase();
          finalName = `${capitalized}-based Product`;
          if (data.extracted_data && !data.extracted_data.name) {
             data.extracted_data.name = finalName;
          } else if (!data.name) {
             data.name = finalName;
          }
        }
      }

      setResult(data);
      
      // Save to recent scans history (max 100)
      if (user) {
        try {
          let history = await getScanHistory(user.uid);
          
          let primaryScore = 0;
          let secondaryScore = 0;
          let primaryLabel = 'Nutri';
          let secondaryLabel = 'AI';
          
          if (scanMode === 'claims') {
             primaryScore = data.verification?.overall_trust_score ?? 0;
             primaryLabel = 'Trust';
             secondaryScore = -1; 
          } else if (scanMode === 'front') {
             primaryScore = data.health_halo?.deception_index ?? 0;
             primaryLabel = 'Decept';
             secondaryScore = -1;
          } else if (scanMode === 'nutrition') {
             primaryScore = -1;
             secondaryScore = -1;
          } else {
             primaryScore = data.score?.nutritional_quality_score ?? 0;
             secondaryScore = data.score?.processing_score ?? 0;
          }

          const newScan = {
            id: Date.now().toString(),
            name: data.extracted_data?.name || data.name || (scanMode === 'claims' ? 'Claims Check' : scanMode === 'front' ? 'Front Label' : scanMode === 'nutrition' ? 'Nutrition Facts' : 'Unnamed Product'),
            scanMode: scanMode,
            score: primaryScore,
            processing_score: secondaryScore,
            metabolic_fit_score: data.biocontext?.metabolic_fit_score ?? data.score?.nutritional_quality_score ?? 0,
            primaryLabel: primaryLabel,
            secondaryLabel: secondaryLabel,
            ingredients: data.extracted_data?.ingredients || [],
            decoded_additives: data.detective?.decoded_additives || [],
            timestamp: new Date().toISOString()
          };
          history.unshift(newScan);
          history = history.slice(0, 100); // Keep last 100 for accurate lifetime averages
          await saveScanHistory(user.uid, history);
        } catch (e) {
          console.error("Failed to save history to Firestore", e);
        }
      }
      
      setStep(4); // Results
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'An error occurred during analysis.');
      setStep(2); // Back to review on error
    }
  };

  const handleAddToBasket = async () => {
    if (!user) {
      setBasketMsg('Please log in to use the Basket feature');
      setTimeout(() => setBasketMsg(''), 3000);
      return;
    }
    if (!result?.extracted_data) return;
    setAddingToBasket(true);
    try {
      const token = await getToken();
      const payloadData = {
        ...result.extracted_data,
        score: result.score,
        biocontext: result.biocontext
      };
      
      const response = await fetch(apiUrl('/api/v1/basket/add', 8007), {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          product_data: payloadData
        }),
      });
      if (!response.ok) throw new Error('Failed to add');
      setBasketMsg('Added successfully!');
      setTimeout(() => setBasketMsg(''), 3000);
    } catch (err) {
      setBasketMsg('Failed to add');
    } finally {
      setAddingToBasket(false);
    }
  };

  if (loading) return null;

  return (
    <SidebarLayout>
      <div className="flex flex-col h-full w-full">

            {/* Step Progress Indicator */}
            <div className="flex items-center justify-center gap-2 sm:gap-4 text-[10px] sm:text-xs font-medium mb-6 py-3 px-4 bg-white rounded-2xl border border-gray-100 shadow-sm">
              <div className={`flex items-center gap-1 sm:gap-2 ${step >= 1 ? 'text-foreground' : 'text-gray-400'}`}>
                <span className={`w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center text-[9px] sm:text-[10px] font-bold ${step >= 1 ? 'bg-brand text-white' : 'bg-gray-100'}`}>1</span>
                <span className="hidden sm:inline">Capture</span>
              </div>
              <div className={`w-6 sm:w-10 h-px ${step >= 2 ? 'bg-brand' : 'bg-gray-200'}`} />
              <div className={`flex items-center gap-1 sm:gap-2 ${step >= 2 ? 'text-foreground' : 'text-gray-400'}`}>
                <span className={`w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center text-[9px] sm:text-[10px] font-bold ${step >= 2 ? 'bg-brand text-white' : 'bg-gray-100'}`}>2</span>
                <span className="hidden sm:inline">Review</span>
              </div>
              <div className={`w-6 sm:w-10 h-px ${step >= 3 ? 'bg-brand' : 'bg-gray-200'}`} />
              <div className={`flex items-center gap-1 sm:gap-2 ${step >= 3 ? 'text-foreground' : 'text-gray-400'}`}>
                <span className={`w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center text-[9px] sm:text-[10px] font-bold ${step >= 3 ? 'bg-brand text-white' : 'bg-gray-100'}`}>3</span>
                <span className="hidden sm:inline">Analyze</span>
              </div>
              <div className={`w-6 sm:w-10 h-px ${step >= 4 ? 'bg-brand' : 'bg-gray-200'}`} />
              <div className={`flex items-center gap-1 sm:gap-2 ${step >= 4 ? 'text-foreground' : 'text-gray-400'}`}>
                <span className={`w-5 h-5 sm:w-6 sm:h-6 rounded-full flex items-center justify-center text-[9px] sm:text-[10px] font-bold ${step >= 4 ? 'bg-brand text-white' : 'bg-gray-100'}`}>4</span>
                <span className="hidden sm:inline">Results</span>
              </div>
            </div>
            
            {error && (
              <div className="mb-6 p-4 bg-red-50 text-red-600 border border-red-100 rounded-xl text-sm font-medium text-center">
                {error}
              </div>
            )}

            {(step === 1 || step === 2) && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-12 h-full min-h-[500px]">
                {/* Left Text / Checklist */}
                <div className="flex flex-col justify-center space-y-8">
                  <div>
                    <h1 className="text-4xl font-serif text-brand mb-4">Scan any food product</h1>
                    <p className="text-sm text-gray-500 leading-relaxed">
                      Capture clear images of the front of the pack, ingredients list, and nutrition facts for complete intelligence.
                    </p>
                  </div>
                  <div className="mb-6">
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-3">Select Scan Mode</label>
                    <div className="flex flex-col gap-3">
                      <button 
                        onClick={() => setScanMode('ingredients')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'ingredients' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'ingredients' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'ingredients' ? 'text-brand-dark' : 'text-gray-700'}`}>Ingredients Analysis</h3>
                            <p className="text-xs text-gray-500">Scan back-of-pack for UPF score & toxicity</p>
                          </div>
                        </div>
                      </button>
                      <button 
                        onClick={() => setScanMode('front')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'front' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'front' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'front' ? 'text-brand-dark' : 'text-gray-700'}`}>Front of Pack</h3>
                            <p className="text-xs text-gray-500">Detect health halos & marketing tricks</p>
                          </div>
                        </div>
                      </button>
                      <button 
                        onClick={() => setScanMode('nutrition')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'nutrition' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'nutrition' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'nutrition' ? 'text-brand-dark' : 'text-gray-700'}`}>Nutrition Facts</h3>
                            <p className="text-xs text-gray-500">Expose portion loopholes & empty calories</p>
                          </div>
                        </div>
                      </button>
                      <button 
                        onClick={() => setScanMode('claims')}
                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${scanMode === 'claims' ? 'border-brand bg-brand-light/30 ring-1 ring-brand' : 'border-gray-200 bg-white hover:border-brand/50'}`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${scanMode === 'claims' ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'}`}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                          </div>
                          <div className="text-left">
                            <h3 className={`text-sm font-bold ${scanMode === 'claims' ? 'text-brand-dark' : 'text-gray-700'}`}>Claims Verifier</h3>
                            <p className="text-xs text-gray-500">Cross-reference marketing with ingredients</p>
                          </div>
                        </div>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Right Viewfinder */}
                <div className="md:col-span-2 bg-white rounded-3xl border border-gray-100 shadow-sm p-8 flex flex-col gap-8 items-center justify-center">
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef}
                     onChange={handleFileChange}
                     className="hidden"
                   />
                   <input 
                     type="file" 
                     accept="image/*" 
                     ref={uploadInputRef2}
                     onChange={handleFile2Change}
                     className="hidden"
                   />
                   
                   <div className="flex flex-col gap-8 w-full items-center">
                     <div className="flex flex-col items-center w-full">
                       {/* Single Main Frame */}
                       <div 
                         className={`relative w-full aspect-[3/4] max-w-sm rounded-2xl border-2 overflow-hidden cursor-pointer transition-colors flex items-center justify-center ${isCameraActive ? 'border-brand bg-gray-50 shadow-lg' : 'border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100'}`}
                         onClick={isCameraActive ? capturePhoto : (step === 1 ? startCamera : undefined)}
                       >
                          {scanMode === 'claims' && isCameraActive && (
                            <div className="absolute top-4 z-10 bg-black/60 text-white px-4 py-1.5 rounded-full text-xs font-bold backdrop-blur-md">
                              {activeClaimsTab === 'back' ? "Capturing Back (Ingredients)" : "Capturing Front of Pack"}
                            </div>
                          )}
                          <video ref={videoRef} autoPlay playsInline className={`w-full h-full object-cover ${isCameraActive ? 'block' : 'hidden'}`} />
                          <canvas ref={canvasRef} className="hidden" />
                          
                          {!isCameraActive && (
                            (scanMode === 'claims' && activeClaimsTab === 'back' ? previewUrl2 : previewUrl) ? (
                              <img src={scanMode === 'claims' && activeClaimsTab === 'back' ? previewUrl2! : previewUrl!} alt="Preview" className="w-full h-full object-cover" />
                            ) : (
                              <div className="text-center p-6">
                                <div className="w-16 h-16 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center mx-auto mb-4 text-gray-400">
                                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /></svg>
                                </div>
                                <h3 className="text-sm font-bold text-gray-900 mb-1">
                                  {scanMode === 'claims' ? (activeClaimsTab === 'back' ? "Ingredients List" : "Front of Pack") : 
                                   scanMode === 'ingredients' ? "Capture Ingredients List" :
                                   scanMode === 'nutrition' ? "Capture Nutrition Facts" :
                                   scanMode === 'front' ? "Capture Front of Pack" :
                                   "Capture Product Label"}
                                </h3>
                                <p className="text-xs text-gray-500">Tap to activate camera</p>
                              </div>
                            )
                          )}
                          
                          {/* Corner markers */}
                          <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-brand"></div>
                          <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-brand"></div>
                          <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-brand"></div>
                          <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-brand"></div>
                       </div>

                       {/* Thumbnails Row */}
                       <div className="flex flex-row gap-6 justify-center mt-8">
                          {scanMode === 'claims' ? (
                            <>
                              <div className="space-y-2 text-center cursor-pointer" onClick={() => setActiveClaimsTab('front')}>
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${activeClaimsTab === 'front' ? 'border-brand' : (previewUrl ? 'border-brand border-solid' : 'border-gray-200 border-dashed')} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors relative`}>
                                  {previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                  {previewUrl && activeClaimsTab !== 'front' && <div className="absolute inset-0 bg-black/20"></div>}
                                </div>
                                <span className={`text-[11px] font-semibold ${activeClaimsTab === 'front' ? 'text-brand' : 'text-gray-500'}`}>Front Pack</span>
                              </div>
                              <div className="space-y-2 text-center cursor-pointer" onClick={() => setActiveClaimsTab('back')}>
                                <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${activeClaimsTab === 'back' ? 'border-brand' : (previewUrl2 ? 'border-brand border-solid' : 'border-gray-200 border-dashed')} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors relative`}>
                                  {previewUrl2 ? <img src={previewUrl2} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                                  {previewUrl2 && activeClaimsTab !== 'back' && <div className="absolute inset-0 bg-black/20"></div>}
                                </div>
                                <span className={`text-[11px] font-semibold ${activeClaimsTab === 'back' ? 'text-brand' : 'text-gray-500'}`}>Ingredients</span>
                              </div>
                            </>
                          ) : (
                            <div className="space-y-2 text-center">
                              <div className={`w-16 h-16 mx-auto rounded-xl border-2 ${previewUrl ? 'border-brand border-solid' : 'border-gray-200 border-dashed'} bg-white overflow-hidden flex items-center justify-center text-[10px] text-gray-300 transition-colors`}>
                                {previewUrl ? <img src={previewUrl} className="w-full h-full object-cover" alt="thumb"/> : 'Empty'}
                              </div>
                              <span className="text-[11px] font-semibold text-gray-500">
                                {scanMode === 'ingredients' ? 'Ingredients Label' : 
                                 scanMode === 'nutrition' ? 'Nutrition Facts' : 
                                 scanMode === 'front' ? 'Front of Pack' : 'Captured Image'}
                              </span>
                            </div>
                          )}
                       </div>
                     </div>
                   </div>

                   {/* Bottom Controls */}
                   <div className="flex justify-center items-center gap-4 mt-4 pt-4 border-t border-gray-100 w-full flex-wrap">
                     <button onClick={step === 1 ? (isCameraActive ? stopCamera : handleRetake) : handleRetake} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-28 text-center">
                       {step === 1 ? (isCameraActive ? 'Cancel' : 'Retake') : 'Retake'}
                     </button>
                     
                     <div 
                        onClick={step === 1 ? (isCameraActive ? capturePhoto : startCamera) : () => processImage(false)}
                        className={`w-16 h-16 rounded-full border-4 border-gray-200 flex items-center justify-center cursor-pointer hover:border-brand transition-colors ${step === 2 ? 'hidden' : ''}`}
                      >
                       <div className={`w-12 h-12 rounded-full shadow-md ${isCameraActive ? 'bg-red-500' : 'bg-brand'}`}></div>
                     </div>
                     
                     {step === 1 && (
                       <button onClick={() => (scanMode === 'claims' && activeClaimsTab === 'back' ? uploadInputRef2.current?.click() : uploadInputRef.current?.click())} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-600 hover:bg-gray-50 transition-colors shadow-sm w-28">
                         Upload
                       </button>
                     )}

                     {step === 2 && (
                       <button onClick={() => processImage(true)} className="px-4 py-2 bg-brand border border-brand rounded-full text-xs font-bold text-white hover:bg-brand-dark transition-colors shadow-sm w-32 flex items-center justify-center gap-2">
                         <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                         Scan
                       </button>
                     )}
                   </div>
                </div>
              </div>
            )}

            {step === 3 && (
              <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full px-4 space-y-8 animate-fade-in">
                <div className="text-center space-y-2">
                  <h2 className="text-2xl font-serif text-brand">Analyzing Product</h2>
                  <p className="text-sm text-gray-500 h-6 transition-all">{progressText}</p>
                </div>
                
                <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden shadow-inner">
                  <div 
                    className="bg-brand h-full rounded-full transition-all duration-75 ease-out relative"
                    style={{ width: `${progress}%` }}
                  >
                    <div className="absolute inset-0 bg-white/20 w-full h-full"></div>
                  </div>
                </div>
                <div className="text-xs font-bold tracking-widest uppercase text-gray-400">
                  {Math.round(progress)}%
                </div>
              </div>
            )}

            {step === 4 && result && (
              <div className="space-y-8 animate-fade-in pb-12">

                 {scanMode === 'nutrition' && result && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Product analysis header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           {isEditingName ? (
                             <div className="flex items-center gap-2 mb-1">
                               <input 
                                 autoFocus
                                 className="text-3xl font-serif bg-transparent border-b border-white/50 focus:border-white outline-none text-white placeholder-white/50 w-full"
                                 value={editNameValue}
                                 onChange={(e) => setEditNameValue(e.target.value)}
                                 onBlur={handleNameSave}
                                 onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
                               />
                             </div>
                           ) : (
                             <div className="flex items-center gap-2 mb-1 group/edit">
                               <h1 className="text-3xl font-serif drop-shadow-md truncate max-w-[300px] md:max-w-[500px]">
                                 {result.extracted_data?.name || result.name || 'Unknown Product'}
                               </h1>
                               <button 
                                 onClick={() => {
                                   setEditNameValue(result.extracted_data?.name || result.name || '');
                                   setIsEditingName(true);
                                 }} 
                                 className="opacity-0 group-hover/edit:opacity-100 p-2 bg-black/20 hover:bg-black/40 rounded-full transition-all backdrop-blur-sm"
                               >
                                 <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                               </button>
                             </div>
                           )}
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Nutrition Panel Analysis • Portion Loopholes</p>
                         </div>
                       </div>
                     </div>

                     {/* Core Metrics Grid */}
                     <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Realistic Serving Size */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" /></svg>
                            Realistic Serving
                          </h2>
                          <div className="relative z-10">
                            <div className="flex items-baseline gap-2 mb-2">
                              <p className={`text-4xl font-serif leading-none ${result.analyzed_serving?.is_loophole ? 'text-red-600' : 'text-brand'}`}>
                                {result.analyzed_serving?.realistic_amount}
                              </p>
                              <span className="text-lg font-bold text-gray-400">{result.analyzed_serving?.unit}</span>
                            </div>
                            {result.analyzed_serving?.is_loophole ? (
                              <span className="inline-block bg-red-100 text-red-700 text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Loophole Exposer: {result.analyzed_serving?.multiplier}x Multiplier</span>
                            ) : (
                              <span className="inline-block bg-brand-light text-brand text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Honest Portion</span>
                            )}
                          </div>
                        </div>

                        {/* Empty Calorie Ratio */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" /></svg>
                            Empty Calorie Ratio
                          </h2>
                          <div className="flex items-end justify-between relative z-10">
                            <div>
                              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-lg font-black text-white shadow-md mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3 ${(result.empty_calorie_ratio?.ratio || 0) > 0.4 ? 'bg-red-500' : 'bg-green-500'}`}>
                                {Math.round((result.empty_calorie_ratio?.ratio || 0) * 100)}%
                              </div>
                              <p className="text-3xl font-serif text-foreground leading-none">{result.empty_calorie_ratio?.empty_calories}</p>
                              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">Empty Cals / 100g</p>
                            </div>
                          </div>
                        </div>

                        {/* Threshold Warnings Count */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                            Threshold Flags
                          </h2>
                          <div className="relative z-10">
                            <p className={`text-4xl font-serif leading-none mb-2 ${result.threshold_warnings?.length > 0 ? 'text-red-600' : 'text-green-600'}`}>
                              {result.threshold_warnings?.length || 0}
                            </p>
                            <span className={`inline-block text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full ${result.threshold_warnings?.length > 0 ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                              {result.threshold_warnings?.length > 0 ? 'High Daily Value' : 'Within Limits'}
                            </span>
                          </div>
                        </div>
                     </div>

                     {/* Detailed Insight Columns */}
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       
                       {/* Left Column: Serving Loophole */}
                       <div className="space-y-6">
                         {result.analyzed_serving && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                               Serving Size Exposer
                             </h2>
                             {result.analyzed_serving.is_loophole ? (
                               <div className="p-4 rounded-xl border-l-4 border-red-500 bg-red-50 mb-4">
                                 <p className="text-sm text-red-800 leading-relaxed font-medium">{result.analyzed_serving.loophole_warning}</p>
                               </div>
                             ) : (
                               <div className="p-4 rounded-xl border-l-4 border-green-500 bg-green-50 mb-4">
                                 <p className="text-sm text-green-800 leading-relaxed font-medium">The stated serving size of {result.stated_serving?.amount}{result.stated_serving?.unit} is realistic.</p>
                               </div>
                             )}
                             <div className="mt-4 pt-4 border-t border-gray-100">
                               <p className="text-xs text-gray-500 mb-1">Stated vs Realistic Comparison:</p>
                               <div className="flex items-center gap-4">
                                 <div className="text-center bg-gray-50 p-2 rounded-lg flex-1">
                                    <span className="block text-[10px] uppercase font-bold text-gray-400">Label Claims</span>
                                    <span className="font-bold text-brand-dark">{result.stated_serving?.amount}{result.stated_serving?.unit}</span>
                                 </div>
                                 <div className="text-gray-300">➜</div>
                                 <div className="text-center bg-brand-light p-2 rounded-lg flex-1">
                                    <span className="block text-[10px] uppercase font-bold text-brand">Actual Portion</span>
                                    <span className="font-bold text-brand">{result.analyzed_serving.realistic_amount}{result.analyzed_serving.unit}</span>
                                 </div>
                               </div>
                             </div>
                           </div>
                         )}
                       </div>

                       {/* Right Column: Threshold Warnings */}
                       <div className="space-y-6">
                         {result.threshold_warnings && result.threshold_warnings.length > 0 ? (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center justify-between">
                               Acceptable Daily Intake (ADI)
                               <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Over Limit</span>
                             </h2>
                             <div className="space-y-3">
                               {result.threshold_warnings.map((warn: any, i: number) => (
                                 <div key={i} className="flex flex-col p-4 bg-red-50/50 rounded-xl border border-red-100 gap-2">
                                   <div className="flex items-center justify-between">
                                     <span className="font-bold text-sm text-red-700">{warn.nutrient}</span>
                                     <span className="text-[10px] uppercase font-bold text-red-600 tracking-widest bg-red-100 px-2 py-1 rounded-full">{warn.percentage_of_adi}% of Daily Limit</span>
                                   </div>
                                   <p className="text-xs text-red-700 leading-relaxed">{warn.warning_message}</p>
                                   <div className="w-full bg-red-100 rounded-full h-1.5 mt-1">
                                     <div className="bg-red-500 h-1.5 rounded-full" style={{width: `${Math.min(100, warn.percentage_of_adi)}%`}}></div>
                                   </div>
                                 </div>
                               ))}
                             </div>
                           </div>
                         ) : (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-center h-full min-h-[200px]">
                              <div className="text-center">
                                <div className="w-12 h-12 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                                </div>
                                <p className="text-sm font-bold text-green-700">No Macro Thresholds Exceeded</p>
                                <p className="text-xs text-gray-500 mt-1">This product is within safe daily limits.</p>
                              </div>
                           </div>
                         )}
                       </div>
                     </div>


                   </div>
                 )}


                 {scanMode === 'claims' && result && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Claims verification header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           {isEditingName ? (
                             <div className="flex items-center gap-2 mb-1">
                               <input 
                                 autoFocus
                                 className="text-3xl font-serif bg-transparent border-b border-white/50 focus:border-white outline-none text-white placeholder-white/50 w-full"
                                 value={editNameValue}
                                 onChange={(e) => setEditNameValue(e.target.value)}
                                 onBlur={handleNameSave}
                                 onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
                               />
                             </div>
                           ) : (
                             <div className="flex items-center gap-2 mb-1 group/edit">
                               <h1 className="text-3xl font-serif drop-shadow-md truncate max-w-[300px] md:max-w-[500px]">
                                 {result.extracted_data?.name || result.name || 'Unknown Product'}
                               </h1>
                               <button 
                                 onClick={() => {
                                   setEditNameValue(result.extracted_data?.name || result.name || '');
                                   setIsEditingName(true);
                                 }} 
                                 className="opacity-0 group-hover/edit:opacity-100 p-2 bg-black/20 hover:bg-black/40 rounded-full transition-all backdrop-blur-sm"
                               >
                                 <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                               </button>
                             </div>
                           )}
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Claims Verifier • Contradictions & Loopholes</p>
                         </div>
                       </div>
                     </div>

                     {/* Contradictions */}
                     {result.verification?.contradictions?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-red-100 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-red-500 mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                           Direct Contradictions
                         </h2>
                         <div className="space-y-4">
                           {result.verification.contradictions.map((c: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-red-200 bg-red-50">
                               <p className="text-lg font-bold text-red-900 mb-1">&quot;{c.claim}&quot;</p>
                               <p className="text-sm text-red-700 font-medium mb-3">But contains: <span className="font-black">{c.contradicting_ingredient}</span></p>
                               <p className="text-xs text-red-600 bg-white px-3 py-2 rounded-lg border border-red-100">{c.explanation}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* Loopholes */}
                     {result.verification?.loopholes?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-yellow-100 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-yellow-600 mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                           Regulatory Loopholes
                         </h2>
                         <div className="space-y-4">
                           {result.verification.loopholes.map((l: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-yellow-200 bg-yellow-50">
                               <p className="text-lg font-bold text-yellow-900 mb-1">&quot;{l.claim}&quot;</p>
                               <p className="text-sm text-yellow-800 font-medium mb-3">Means: <span className="font-black">{l.true_meaning}</span></p>
                               <p className="text-xs text-yellow-700 bg-white px-3 py-2 rounded-lg border border-yellow-100">{l.reality_check}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* Buzzwords */}
                     {result.verification?.buzzwords?.length > 0 && (
                       <div className="bg-white p-6 rounded-3xl border border-brand/20 shadow-sm relative overflow-hidden">
                         <h2 className="text-xs font-bold uppercase tracking-widest text-brand mb-4 flex items-center gap-2">
                           <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" /></svg>
                           Marketing Fluff
                         </h2>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           {result.verification.buzzwords.map((b: any, i: number) => (
                             <div key={i} className="p-4 rounded-xl border border-brand/10 bg-brand-light/30">
                               <div className="flex justify-between items-center mb-2">
                                 <p className="text-md font-bold text-brand-dark">&quot;{b.word}&quot;</p>
                                 <span className="text-[10px] font-bold uppercase tracking-widest bg-brand text-white px-2 py-0.5 rounded-full">Fluff: {b.fluff_score}%</span>
                               </div>
                               <p className="text-xs text-gray-700 leading-relaxed">{b.explanation}</p>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* All Clear state */}
                     {result.verification?.contradictions?.length === 0 && result.verification?.loopholes?.length === 0 && result.verification?.buzzwords?.length === 0 && (
                       <div className="bg-white p-8 rounded-3xl border border-green-100 shadow-sm text-center">
                         <div className="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                           <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                         </div>
                         <h2 className="text-xl font-bold text-green-800 mb-2">Clean Marketing</h2>
                         <p className="text-sm text-gray-600">No major contradictions, loopholes, or fluff detected between the front claims and the ingredients list.</p>
                       </div>
                     )}

                     {/* Detailed Claims Audit */}
                     <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm mt-8">
                       <h2 className="text-xl font-serif text-gray-900 mb-6 flex items-center gap-2">
                         <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
                         Detailed Claims Audit
                       </h2>
                       <div className="space-y-4">
                         {result.explicit_claims?.length > 0 ? result.explicit_claims.map((claim: string, i: number) => {
                           const contradiction = result.verification?.contradictions?.find((c: any) => c.claim === claim);
                           const loophole = result.verification?.loopholes?.find((l: any) => l.claim === claim);
                           const buzzword = result.verification?.buzzwords?.find((b: any) => b.word === claim);

                           let status = 'CLEAN';
                           if (contradiction) status = 'CONTRADICTION';
                           else if (loophole) status = 'LOOPHOLE';
                           else if (buzzword) status = 'BUZZWORD';

                           return (
                             <div key={i} className={`p-5 rounded-2xl border ${status === 'CLEAN' ? 'border-green-100 bg-green-50' : status === 'CONTRADICTION' ? 'border-red-100 bg-red-50' : status === 'LOOPHOLE' ? 'border-yellow-100 bg-yellow-50' : 'border-brand/20 bg-brand-light/30'}`}>
                               <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                                 <p className="text-lg font-bold text-gray-900">&quot;{claim}&quot;</p>
                                 <div>
                                   {status === 'CLEAN' && <span className="text-[10px] font-bold uppercase tracking-widest bg-green-200 text-green-800 px-3 py-1 rounded-full">No Flags Detected</span>}
                                   {status === 'CONTRADICTION' && <span className="text-[10px] font-bold uppercase tracking-widest bg-red-200 text-red-800 px-3 py-1 rounded-full">Direct Contradiction</span>}
                                   {status === 'LOOPHOLE' && <span className="text-[10px] font-bold uppercase tracking-widest bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full">Regulatory Loophole</span>}
                                   {status === 'BUZZWORD' && <span className="text-[10px] font-bold uppercase tracking-widest bg-brand text-white px-3 py-1 rounded-full">Marketing Fluff</span>}
                                 </div>
                               </div>
                               
                               <div className="text-sm">
                                 {status === 'CLEAN' && <p className="text-green-700">This claim appears to be standard and does not trigger our deception database.</p>}
                                 
                                 {status === 'CONTRADICTION' && (
                                   <>
                                     <p className="text-red-700 font-medium mb-2">But contains: <span className="font-black">{contradiction.contradicting_ingredient}</span></p>
                                     <p className="text-red-600 bg-white px-4 py-3 rounded-xl border border-red-100 leading-relaxed">{contradiction.explanation}</p>
                                   </>
                                 )}
                                 
                                 {status === 'LOOPHOLE' && (
                                   <>
                                     <p className="text-yellow-800 font-medium mb-2">Means: <span className="font-black">{loophole.true_meaning}</span></p>
                                     <p className="text-yellow-700 bg-white px-4 py-3 rounded-xl border border-yellow-100 leading-relaxed">{loophole.reality_check}</p>
                                   </>
                                 )}
                                 
                                 {status === 'BUZZWORD' && (
                                   <p className="text-gray-700 bg-white px-4 py-3 rounded-xl border border-brand/10 leading-relaxed">{buzzword.explanation}</p>
                                 )}
                               </div>
                             </div>
                           );
                         }) : (
                           <div className="bg-gray-50 border border-gray-100 rounded-2xl p-6 text-center">
                             <p className="text-gray-500 font-medium">No explicit marketing claims detected on the front of the packaging.</p>
                           </div>
                         )}
                       </div>
                     </div>



                   </div>
                 )}

                 {scanMode === 'front' && (
                   <div className="space-y-8">
                     {/* Hero Header */}
                     <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                       <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Product analysis header" />
                       <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                       <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                         <div className="text-white">
                           {isEditingName ? (
                             <div className="flex items-center gap-2 mb-1">
                               <input 
                                 autoFocus
                                 className="text-3xl font-serif bg-transparent border-b border-white/50 focus:border-white outline-none text-white placeholder-white/50 w-full"
                                 value={editNameValue}
                                 onChange={(e) => setEditNameValue(e.target.value)}
                                 onBlur={handleNameSave}
                                 onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
                               />
                             </div>
                           ) : (
                             <div className="flex items-center gap-2 mb-1 group/edit">
                               <h1 className="text-3xl font-serif drop-shadow-md truncate max-w-[300px] md:max-w-[500px]">
                                 {result.extracted_data?.name || result.name || 'Unknown Product'}
                               </h1>
                               <button 
                                 onClick={() => {
                                   setEditNameValue(result.extracted_data?.name || result.name || '');
                                   setIsEditingName(true);
                                 }} 
                                 className="opacity-0 group-hover/edit:opacity-100 p-2 bg-black/20 hover:bg-black/40 rounded-full transition-all backdrop-blur-sm"
                               >
                                 <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                               </button>
                             </div>
                           )}
                           <p className="text-sm text-white/90 font-medium drop-shadow-sm">Front of Pack • Marketing & Deception</p>
                         </div>
                       </div>
                     </div>

                     {/* Core Metrics Grid */}
                     <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Deception Index */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                            Health Halo Deception
                          </h2>
                          <div className="flex items-end justify-between relative z-10">
                            <div>
                              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-xl font-black text-white shadow-md mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3 ${(result.health_halo?.deception_index || 0) > 70 ? 'bg-red-500' : ((result.health_halo?.deception_index || 0) > 40 ? 'bg-yellow-500' : 'bg-green-500')}`}>
                                {(result.health_halo?.deception_index || 0) > 70 ? 'HIGH' : ((result.health_halo?.deception_index || 0) > 40 ? 'MOD' : 'LOW')}
                              </div>
                              <p className="text-3xl font-serif text-foreground leading-none">{result.health_halo?.deception_index || 0}</p>
                              <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">/ 100 Index</p>
                            </div>
                          </div>
                        </div>

                        {/* Target Audience */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                            Primary Demographic
                          </h2>
                          <div className="relative z-10">
                            <p className="text-xl font-bold text-foreground leading-tight mb-2">{result.target_audience?.demographic || 'General'}</p>
                            <span className="inline-block bg-brand-light text-brand text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded-full">Target Detected</span>
                          </div>
                        </div>

                        {/* Explicit Claims */}
                        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                          <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                            Explicit Claims
                          </h2>
                          <div className="relative z-10 flex flex-wrap gap-2">
                             {result.explicit_claims?.length > 0 ? result.explicit_claims.slice(0, 3).map((claim: string, i: number) => (
                               <span key={i} className="text-[9px] font-bold uppercase tracking-widest bg-blue-50 border border-blue-100 text-blue-700 px-2 py-1 rounded-md">{claim}</span>
                             )) : (
                               <span className="text-xs text-gray-400 font-medium italic">No claims detected</span>
                             )}
                          </div>
                        </div>
                     </div>

                     {/* Main Insights Columns */}
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       
                       {/* Left Column: Visual Analysis */}
                       <div className="space-y-6">
                         {result.health_halo && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center gap-2">
                               Health Halo Breakdown
                             </h2>
                             <div className="p-4 rounded-xl border-l-4 border-yellow-500 bg-yellow-50 mb-4">
                               <p className="text-sm text-yellow-800 leading-relaxed font-medium">{result.health_halo.reasoning}</p>
                             </div>
                             {result.health_halo.visual_cues && result.health_halo.visual_cues.length > 0 && (
                               <div className="mt-4 pt-4 border-t border-gray-100">
                                 <h3 className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-3">Detected Visual Cues</h3>
                                 <div className="flex flex-wrap gap-2">
                                   {result.health_halo.visual_cues.map((cue: string, i: number) => (
                                     <span key={i} className="text-[10px] font-bold uppercase tracking-widest bg-gray-100 text-gray-600 px-3 py-1.5 rounded-full">{cue}</span>
                                   ))}
                                 </div>
                               </div>
                             )}
                           </div>
                         )}
                       </div>

                       {/* Right Column: Audience Concerns & Prominent Ingredients */}
                       <div className="space-y-6">
                         {result.target_audience?.concerns && result.target_audience.concerns.length > 0 && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex items-center justify-between">
                               Audience Concerns
                               <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Flagged</span>
                             </h2>
                             <div className="space-y-3">
                               {result.target_audience.concerns.map((con: string, i: number) => (
                                 <div key={i} className="flex items-start gap-3 p-3 bg-red-50/50 rounded-xl border border-red-100">
                                   <span className="text-red-500 mt-0.5">⚠</span>
                                   <p className="text-xs text-red-700 leading-relaxed">{con}</p>
                                 </div>
                               ))}
                             </div>
                           </div>
                         )}
                         
                         {result.prominent_ingredients && result.prominent_ingredients.length > 0 && (
                           <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                             <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4">Ingredient Illusions</h2>
                             <div className="space-y-3">
                               {result.prominent_ingredients.map((ing: any, i: number) => (
                                 <div key={i} className="flex flex-col p-4 bg-white rounded-xl border border-gray-100 shadow-sm gap-2">
                                   <div className="flex items-center justify-between border-b border-gray-50 pb-2">
                                     <span className="font-bold text-sm text-foreground">{ing.name}</span>
                                     <span className="text-[9px] uppercase font-bold text-brand tracking-widest bg-brand-light px-2 py-1 rounded-full">Front Tag</span>
                                   </div>
                                   <div className="text-xs text-gray-600 mt-1">
                                     <span className="font-bold text-gray-400 uppercase text-[9px] tracking-widest block mb-1">Marketing Implication</span>
                                     {ing.implied_quantity}
                                   </div>
                                   <div className="text-xs text-gray-600 mt-2 p-2 bg-gray-50 rounded-lg">
                                     <span className="font-bold text-gray-400 uppercase text-[9px] tracking-widest block mb-1">Reality Check</span>
                                     {ing.reality_check}
                                   </div>
                                 </div>
                               ))}
                             </div>
                           </div>
                         )}
                       </div>
                     </div>


                   </div>
                 )}

                 {scanMode === 'ingredients' && (
                   <>
                 {/* Hero Header */}
                 <div className="relative w-full h-48 rounded-3xl overflow-hidden mb-8 shadow-sm group">
                   <img src="/assets/bg/scan-results.png" className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" alt="Product analysis header" />
                   <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                   
                   <div className="absolute bottom-0 left-0 w-full p-6 flex justify-between items-end">
                     <div className="text-white">
                       {isEditingName ? (
                         <div className="flex items-center gap-2 mb-1">
                           <input 
                             autoFocus
                             className="text-3xl font-serif bg-transparent border-b border-white/50 focus:border-white outline-none text-white placeholder-white/50 w-full"
                             value={editNameValue}
                             onChange={(e) => setEditNameValue(e.target.value)}
                             onBlur={handleNameSave}
                             onKeyDown={(e) => e.key === 'Enter' && handleNameSave()}
                           />
                         </div>
                       ) : (
                         <div className="flex items-center gap-2 mb-1 group/edit">
                           <h1 className="text-3xl font-serif drop-shadow-md truncate max-w-[300px] md:max-w-[500px]">
                             {result.extracted_data?.name || result.name || 'Unknown Product'}
                           </h1>
                           <button 
                             onClick={() => {
                               setEditNameValue(result.extracted_data?.name || result.name || '');
                               setIsEditingName(true);
                             }} 
                             className="opacity-0 group-hover/edit:opacity-100 p-2 bg-black/20 hover:bg-black/40 rounded-full transition-all backdrop-blur-sm"
                           >
                             <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                           </button>
                         </div>
                       )}
                       <p className="text-sm text-white/90 font-medium drop-shadow-sm">{result.extracted_data?.brand || 'Unknown Brand'} • {result.extracted_data?.category || 'Uncategorized'}</p>
                     </div>
                     <div className="flex flex-col items-end">
                       <button 
                         onClick={handleAddToBasket} 
                         disabled={addingToBasket}
                         className="px-6 py-2 bg-white text-brand rounded-xl text-sm font-bold hover:bg-gray-50 hover:scale-105 active:scale-95 disabled:opacity-50 transition-all shadow-md"
                       >
                         {addingToBasket ? 'Adding...' : 'Add to Basket'}
                       </button>
                       {basketMsg && <span className="text-xs text-white mt-2 font-medium bg-black/40 backdrop-blur-sm px-3 py-1 rounded-full">{basketMsg}</span>}
                     </div>
                   </div>
                 </div>

                 {/* Core Metrics Grid */}
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Nutri-Score Widget */}
                    {result.score && (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                        <div className="absolute -right-6 -top-6 w-24 h-24 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex items-center gap-1.5">
                          <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
                          Nutritional Quality
                        </h2>
                        
                        <div className="flex items-end justify-between relative z-10">
                          <div>
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-black text-white shadow-md mb-3 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3 ${getGrade(result.score.nutritional_quality_score).fill || 'bg-brand'}`}>
                              {getGrade(result.score.nutritional_quality_score).letter}
                            </div>
                            <p className="text-3xl font-serif text-foreground leading-none">{result.score.nutritional_quality_score}</p>
                            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mt-1">/ 100 Score</p>
                          </div>
                          
                          <div className="text-right">
                            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold shadow-sm ${getGrade(result.score.nutritional_quality_score).bg} ${getGrade(result.score.nutritional_quality_score).color}`}>
                              Grade {getGrade(result.score.nutritional_quality_score).letter}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* NOVA ML Widget */}
                    {result.score && (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                        <div className="absolute -left-6 -bottom-6 w-32 h-32 bg-gray-50 rounded-full opacity-50 group-hover:scale-110 transition-transform"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-6 relative z-10 flex justify-between items-center">
                          <span className="flex items-center gap-1.5">
                            <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                            Formulation Quality
                          </span>
                          <span className="bg-brand text-white px-2 py-0.5 rounded text-[8px] tracking-widest shadow-sm animate-pulse">AI MODEL</span>
                        </h2>
                        
                        <div className="flex flex-col justify-end h-full relative z-10">
                           <p className="text-3xl font-serif text-foreground leading-none mb-2">{result.score.processing_score}</p>
                           
                           {/* Progress Bar */}
                           <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden mb-3">
                             <div className={`h-full rounded-full transition-all duration-1000 ease-out ${getFormulationTier(result.score.processing_score).fill}`} style={{ width: `${result.score.processing_score}%` }}></div>
                           </div>
                           
                           <div className="flex justify-between items-center">
                             <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Nourient AI</p>
                             <span className={`text-[10px] font-bold uppercase tracking-widest ${getFormulationTier(result.score.processing_score).color}`}>
                               {getFormulationTier(result.score.processing_score).label}
                             </span>
                           </div>
                        </div>
                      </div>
                    )}

                    {/* Metabolic Fit Widget */}
                    {result.biocontext ? (
                      <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col justify-between relative overflow-hidden group hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                        <div className="absolute right-0 top-0 w-full h-full bg-gradient-to-br from-white to-brand-light/30 opacity-50 group-hover:opacity-70 transition-opacity duration-300"></div>
                        <h2 className="text-[10px] font-bold uppercase tracking-widest text-gray-500 mb-4 relative z-10 flex items-center gap-1.5">
                          <svg className="w-3 h-3 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                          Metabolic Fit
                        </h2>
                        
                        <div className="relative z-10 flex flex-col h-full justify-between">
                          <div>
                            <div className="flex items-center gap-2 mb-2">
                              <span className="relative flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand opacity-40"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-brand"></span>
                              </span>
                              <span className="text-xs font-bold text-brand uppercase tracking-widest">{result.biocontext.health_profile}</span>
                            </div>
                            <p className="text-3xl font-serif text-brand leading-none mb-1 group-hover:scale-105 origin-left transition-transform duration-300">{result.biocontext.metabolic_fit_score}</p>
                          </div>
                          
                          <p className="text-xs text-gray-600 leading-snug line-clamp-2" title={result.biocontext.context_reasoning}>
                            {result.biocontext.context_reasoning}
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-gray-50 p-6 rounded-3xl border border-dashed border-gray-200 flex flex-col items-center justify-center text-center group hover:bg-gray-100 transition-colors duration-300">
                         <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center mb-3 text-gray-400 group-hover:text-gray-500 transition-colors">
                           <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                         </div>
                         <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-1">Metabolic Fit</h3>
                         <p className="text-[10px] text-gray-400">Sign in to unlock personalized metabolic scoring.</p>
                      </div>
                    )}
                 </div>

                 {/* Recommendation Banner */}
                 {result.score && (
                   <div className={`p-4 rounded-2xl border flex items-center justify-between ${result.score.overall_recommendation.includes('LIMIT') ? 'bg-red-50 border-red-100' : 'bg-brand-light border-brand/20'}`}>
                     <div className="flex items-center gap-4">
                       <div className={`w-10 h-10 rounded-full flex items-center justify-center ${result.score.overall_recommendation.includes('LIMIT') ? 'bg-red-100 text-red-600' : 'bg-white text-brand'}`}>
                         <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                       </div>
                       <div>
                         <p className={`text-xs font-bold uppercase tracking-widest mb-1 ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-700' : 'text-brand'}`}>Nourient&apos;s Recommendation</p>
                         <p className={`text-lg font-serif leading-none ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-900' : 'text-brand-dark'}`}>{result.score.overall_recommendation}</p>
                       </div>
                     </div>
                     {/*<p className={`text-xs max-w-md hidden md:block ${result.score.overall_recommendation.includes('LIMIT') ? 'text-red-600/80' : 'text-brand-dark/80'}`}>
                       {result.score.reasoning}
                     </p>*/}


                   </div>
                 )}

                 <div className="grid grid-cols-1 gap-6">

                    {/* TrueLabel Auditor */}
                    {result.extracted_data?.audit && (
                      <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm h-full">
                        <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-6">TrueLabel Auditor</h2>
                        <div className="space-y-4">
                          {result.extracted_data.audit.map((audit: any, idx: number) => (
                            <div key={idx} className={`p-4 rounded-xl border-l-4 ${audit.verdict === 'Deceptive' ? 'border-red-500 bg-red-50' : 'border-green-500 bg-brand-light'}`}>
                              <div className="flex justify-between items-start mb-2">
                                <span className="font-bold text-sm text-foreground">&quot;{audit.claim}&quot;</span>
                                <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-1 rounded-full ${audit.verdict === 'Deceptive' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-brand'}`}>
                                  {audit.verdict}
                                </span>
                              </div>
                              <p className="text-xs text-gray-600">{audit.reasoning}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                 </div>

                 {/* Ingredient Detective */}
                 {result.detective && (
                   <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                     <h2 className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-4 flex justify-between items-center">
                       Ingredient Detective
                       {(result.detective.flagged_ingredients?.length > 0 || result.detective.decoded_additives?.length > 0) && (
                         <span className="bg-red-50 text-red-600 px-2 py-1 rounded-full text-[10px]">Active</span>
                       )}
                     </h2>
                     <p className="text-sm text-gray-600 mb-6 leading-relaxed border-b border-gray-100 pb-6">
                       <span className="font-bold block mb-2 text-xs text-gray-400 uppercase tracking-widest">Raw Ingredient List</span>
                       {result.extracted_data?.ingredients?.map((ing: any) => 
                         ing.percentage ? `${ing.name} (${ing.percentage}%)` : ing.name
                       ).join(', ') || 'No ingredients detected.'}
                     </p>

                     {/* Deterministic Unified Decoder */}
                     {result.detective.decoded_additives?.length > 0 && (
                       <div className="mb-8">
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Ingredients Decoded</h3>
                         <div className="space-y-2">
                           {result.detective.decoded_additives.map((additive: any, i: number) => (
                             <div key={i} className="flex flex-col md:flex-row md:items-center justify-between p-3 bg-white rounded-xl border border-gray-100 shadow-sm gap-4">
                               <div className="flex-1 min-w-0">
                                 <div className="flex items-center gap-2">
                                   <span className="font-bold text-sm text-foreground truncate">{additive.name}</span>
                                   {additive.code && <span className="text-[10px] text-gray-500 font-mono bg-gray-50 border border-gray-200 px-1.5 py-0.5 rounded shrink-0">{additive.code}</span>}
                                 </div>
                               </div>
                               <div className="flex flex-col sm:flex-row items-center gap-2 shrink-0">
                                 <span className="w-full sm:w-[130px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.source}</span>
                                 <span className="w-full sm:w-[150px] text-[9px] uppercase font-bold text-gray-500 tracking-widest bg-gray-50 border border-gray-100 px-2 py-1 rounded-full text-center shrink-0">{additive.category}</span>
                                 <span className={`w-full sm:w-[100px] text-[9px] uppercase font-bold tracking-widest px-2 py-1 rounded-full text-center shrink-0 ${
                                   additive.risk_level.toLowerCase() === 'safe' ? 'bg-green-100 text-green-700 border border-green-200' :
                                   additive.risk_level.toLowerCase() === 'moderate risk' || additive.risk_level.toLowerCase() === 'permitted additive' ? 'bg-yellow-100 text-yellow-700 border border-yellow-200' :
                                   additive.risk_level.toLowerCase() === 'unknown' ? 'bg-gray-100 text-gray-600 border border-gray-200' :
                                   'bg-red-100 text-red-700 border border-red-200'
                                 }`}>
                                   {additive.risk_level}
                                 </span>
                               </div>
                             </div>
                           ))}
                         </div>
                       </div>
                     )}

                     {/* AI Flagger */}
                     {result.detective.flagged_ingredients?.length > 0 && (
                       <div>
                         <h3 className="font-bold text-xs text-foreground uppercase tracking-widest mb-3">Flagged Concerns</h3>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                           {result.detective.flagged_ingredients.map((ing: any, i: number) => (
                             <div key={i} className="p-4 bg-red-50 rounded-xl border border-red-100">
                               <div className="flex justify-between items-center mb-2">
                                 <span className="font-bold text-sm text-red-700">{ing.name}</span>
                                 <span className="text-[10px] uppercase font-bold text-red-700 tracking-widest bg-red-100 px-2 py-1 rounded-full">{ing.purpose}</span>
                               </div>
                               <p className="text-xs text-red-600 mb-1">{ing.warning || ing.explanation}</p>
                               {ing.studies && <p className="text-[10px] text-red-400 italic mt-2 border-t border-red-100 pt-2">Studies: {ing.studies}</p>}
                             </div>
                           ))}
                         </div>
                       </div>
                     )}


                   </div>
                 )}
                 
                 <div className="flex justify-center mt-8">
                   <button onClick={handleRetake} className="px-6 py-2 border border-gray-200 bg-white rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                     Scan Another Product
                   </button>
                 </div>
                 </>
                 )}
              </div>
            )}

      </div>
    </SidebarLayout>
  );
}
