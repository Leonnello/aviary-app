<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\VisaApplication;

class VisaApplicationController extends Controller
{
    public function index() {
        return VisaApplication::all();
    }

    public function store(Request $request) {
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'status' => 'required|string',
            'approval_score' => 'required|integer',
        ]);

        return VisaApplication::create($request->all());
    }

    public function show($id) {
        return VisaApplication::findOrFail($id);
    }

    public function update(Request $request, $id) {
        $visaApplication = VisaApplication::findOrFail($id);
        $visaApplication->update($request->all());
        return $visaApplication;
    }

    public function destroy($id) {
        return VisaApplication::destroy($id);
    }
}