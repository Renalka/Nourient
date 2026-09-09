import re

with open('frontend/src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

bad_insertion = """                       </div>
                     )}

                   {/* Bottom Controls */}"""

correct_insertion = """                     )}

                   {/* Bottom Controls */}"""

# The closing tags inside the `) : (` block currently look like:
#                      </div>
#                    </div>
# 
#                        </div>
#                      )}

# Let's just fix it with regex. We want to remove the `</div> \n )}` block before Bottom Controls, 
# and put `)}` right after the inner `</div>` (the one closing the `flex flex-col items-center w-full` wrapper).

# Let's just do a string replacement of the specific messed up area.
messed_up = """                        <div className="space-y-2 text-center cursor-pointer">
                          <div className="w-16 h-16 mx-auto rounded-xl border border-gray-200 bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 transition-colors">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                          </div>
                          <span className="text-[11px] font-semibold text-gray-500">Add claims</span>
                        </div>
                     </div>
                   </div>

                       </div>
                     )}

                   {/* Bottom Controls */}"""

fixed = """                        <div className="space-y-2 text-center cursor-pointer">
                          <div className="w-16 h-16 mx-auto rounded-xl border border-gray-200 bg-gray-50 flex items-center justify-center text-gray-400 hover:bg-gray-100 transition-colors">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                          </div>
                          <span className="text-[11px] font-semibold text-gray-500">Add claims</span>
                        </div>
                     </div>
                     </div>
                   )}
                   </div>

                   {/* Bottom Controls */}"""

content = content.replace(messed_up, fixed)

with open('frontend/src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
